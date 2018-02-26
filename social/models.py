from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class SocialUser(AbstractUser, models.Model):

    @property
    def fullname(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.fullname


class Post(models.Model):
    user = models.ForeignKey(SocialUser, related_name="posts")

    title = models.TextField(unique=True)
    added = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    liked = models.IntegerField(default=0)
    unliked = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

