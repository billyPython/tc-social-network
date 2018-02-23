from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from social.models import SocialUser, Post


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators = [UniqueValidator(queryset=SocialUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=SocialUser.objects.all())]

    )
    password = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'username',
            'password'
        )


class SocialUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField('_get_full_name')

    def _get_full_name(self, obj):
        return obj.fullname

    class Meta:
        model = get_user_model()
        fields = (
            '__all__'
        )


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            '__all__'
        )

