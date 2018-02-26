import os

from django.core.management.base import BaseCommand
from rest_framework import request
from rest_framework.utils import json

from social.models import Post, SocialUser
from social_bot.sbot import SocialBot


class Command(BaseCommand):
    help = "Bot command that sets users, posts and likes"
    BASEDIR = os.getcwd()

    def add_arguments(self, parser):
        parser.add_argument('--data', nargs='?', type=str)

    def handle(self, *args, **options):
        data = json.load(open(options.get("data"), 'r'))
        bot = SocialBot(json_data=data)

        bot.signup_users()
        bot.login_users()
        bot.create_posts()

        posts = Post.objects.all()
        users = SocialUser.objects.all()

        while posts.filter(liked=0):
            bot.like_logic()

        # bot.like_posts()

        pass
