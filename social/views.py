from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from social.models import SocialUser, Post
from social.permissions import UserIsOwner
from social.serializers import SocialUserSerializer, PostSerializer, SignUpSerializer
from social.utils import ehunter


class UserViewSet(ModelViewSet):
    serializer_class = SocialUserSerializer
    queryset = SocialUser.objects.all().order_by('last_login')
    permission_classes = (
        IsAuthenticated,
        UserIsOwner,
    )


class PostViewSet(ModelViewSet):
    """
        View where you can create, like and unlike post.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('added')

    @detail_route(methods=['POST'], )
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        post.liked += 1
        post.save()

        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['POST'])
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        post.unliked += 1
        post.save()

        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request, *args, **kwargs):
    """
        Custom view for registering user on social-network app,
        by checking if their input is valid and is not missing.
    """
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        response = ehunter.email_verifier(serializer.validated_data.get("email"))
        if response['result'] == 'undeliverable':
            return Response('Email does not exist!',status=status.HTTP_400_BAD_REQUEST)

        SocialUser.objects.create_user(**serializer.validated_data)
        return Response("Signup success!", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request, *args, **kwargs):
    """

    """
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

    if not user:
        return Response({"error": "Login failed. Incorrect username or password."}, status=HTTP_401_UNAUTHORIZED)

    payload = jwt_payload_handler(user)
    jwt_token = jwt_encode_handler(payload)

    return Response({"token": jwt_token})

