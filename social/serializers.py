from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from social.models import SocialUser, Post


class SocialUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators = [UniqueValidator(queryset=SocialUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=SocialUser.objects.all())]

    )
    password = serializers.CharField(max_length=128, required=True)
    fullname = serializers.SerializerMethodField('_get_full_name')

    def _get_full_name(self, obj):
        return obj.fullname

    class Meta:
        model = get_user_model()
        fields = (
            'fullname',
            'id',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'username',
            'password'
        )

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            '__all__'
        )

