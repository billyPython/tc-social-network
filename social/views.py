from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet

from social.models import SocialUser, Post
from social.serializers import SocialUserSerializer, PostSerializer


class UserViewSet(ModelViewSet):
    serializer_class = SocialUserSerializer
    queryset = SocialUser.objects.all()
    permission_classes = (IsAdminUser,)


class PostViewSet(ModelViewSet):
    """
        View where you can create, like and unlike post.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @detail_route(methods=['POST'], )
    def like(self, request, *args, **kwargs):
        pass

    @detail_route(methods=['POST'])
    def unlike(self, request, *args, **kwargs):
        pass


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request, *args, **kwargs):
    serializer = SocialUserSerializer(data=request.data)
    if serializer.is_valid():
        SocialUser.objects.create_user(**serializer.validated_data)
        return Response("Signup success!", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request, *args, **kwargs):
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

