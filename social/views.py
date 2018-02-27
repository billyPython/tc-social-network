import base64
from copy import deepcopy

import clearbit
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        request.data.update({"user": request.user.pk})
        return super(PostViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=['GET'], )
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        post.liked += 1
        post.save()

        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['GET'], )
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
    data = deepcopy(request.data)

    # If it is not SocialBot then check if email is valid and enrich it, if possible
    bot_check = base64.b64decode(data.pop('bot', '')).decode('utf-8') == settings.BOT_SECRET_NAME
    if not bot_check:
        ehunter_response = ehunter.email_verifier(data.get("email"))
        if ehunter_response['result'] == 'undeliverable':
            return Response('Email does not exist!', status=status.HTTP_400_BAD_REQUEST)

        clearbit_response = clearbit.Enrichment.find(email=data["email"], stream=True)
        if clearbit_response.get('person'):
            data.update({
                        "first_name": clearbit_response['person']['name']['givenName'],
                        "last_name": clearbit_response['person']['name']['familyName'],
                    })

    serializer = SignUpSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    SocialUser.objects.create_user(**serializer.validated_data)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request, *args, **kwargs):
    """
        Custom login.
        NOTE: Currently rest_auth login is being used not this one.
    """
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

    if not user:
        return Response({"error": "Login failed. Incorrect username or password."}, status=HTTP_401_UNAUTHORIZED)

    user.last_login = timezone.now()
    user.save()
    payload = jwt_payload_handler(user)
    jwt_token = jwt_encode_handler(payload)

    return Response({"token": jwt_token})

