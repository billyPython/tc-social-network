import base64
import random
import string

import requests
from rest_framework import status
from rest_framework.utils import json
import username_generator

from social_bot.exceptions import BotLikeException, BotCreatePostException, BotLoginExcpetion, BotSignUpException


class SocialBot(object):
    HEADERS = {
        "content-type": "application/json",
        "Authorization": ""
    }

    SIGN_UP_URL = 'http://localhost:8000/sign-up/'
    LOGIN_URL = 'http://localhost:8000/login/'
    GET_OR_CREATE_POST_URL = 'http://localhost:8000/api/posts/'

    PWD_GEN_CHARS = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"

    def __init__(self, json_data=None, file_path=None):
        if json_data:
            self.json = json_data
        elif file_path:
            self.json = json.load(open(file_path,'r'))
        else:
            # TODO: make custom exception
            raise Exception

        self.number_of_users = self.json['number_of_users'] if self.json['number_of_users'] else 1
        self.max_posts_per_user = self.json['max_posts_per_user'] if self.json['max_posts_per_user'] else 1
        self.max_likes_per_user = self.json['max_likes_per_user'] if self.json['max_likes_per_user'] else 1


    @staticmethod
    def _pw_gen(size=8, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def _all_posts_liked(posts):
        num_of_posts = len(posts)
        if len([post for post in posts if post['liked'] > 0]) == num_of_posts:
            return True
        else:
            return False

    @staticmethod
    def _no_likes_check(posts, post_owner):
        if [post for post in posts if (post['user'] == post_owner) and (post['liked'] <= 0)]:
            return True
        else:
            return False

    def _get_posts(self, user):
        self.HEADERS['Authorization'] = 'Bearer ' + user['token']
        response = requests.get(url=self.GET_OR_CREATE_POST_URL, headers=self.HEADERS)
        return json.loads(response.content)


    def signup_users(self):
        """
            Sign up random generated users/bots and let signup view know that it is a bot
        """
        self.signed_up_users = []
        number_of_users = self.json['number_of_users']
        while number_of_users:
            username = username_generator.get_uname(min_size=4, max_size=12, underscores=True)

            payload = {
                "bot": base64.b64encode(b'botcuga').decode('utf-8'),
                "username": username,
                "password": self._pw_gen(),
                "email": username + '@bot.com'
            }

            response = requests.post(url=self.SIGN_UP_URL, data=json.dumps(payload), headers=self.HEADERS)

            if not response.status_code == status.HTTP_201_CREATED:
                raise BotSignUpException(response.content)

            self.signed_up_users.append(payload)

            number_of_users -=1

    def login_users(self):
        """
            Login all singed up users and store them in "logged_users"
        """
        self.logged_users = []
        for user in self.signed_up_users:
            response = requests.post(url=self.LOGIN_URL, data=json.dumps(user), headers=self.HEADERS)

            if not response.status_code == status.HTTP_200_OK:
                raise BotLoginExcpetion(response.content)

            self.logged_users.append(json.loads(response.content))

    def create_posts(self):
        """
            Create random number , no greater then max_posts_per_user, for every user. Every post will be
            stored on logged_users data as "posts".
        """
        for user in self.logged_users:

            rand_posts = random.randint(1,self.max_posts_per_user)
            user['posts'] = []

            while rand_posts:
                self.HEADERS['Authorization'] = 'Bearer '+ user['token']

                payload = {
                    "title": user['user']['username'] + " post number " + str(rand_posts),
                    "text": "They see me botting :D"
                }

                response = requests.post(
                                url=self.GET_OR_CREATE_POST_URL,
                                data=json.dumps(payload),
                                headers=self.HEADERS
                            )

                if not response.status_code == status.HTTP_201_CREATED:
                    raise BotCreatePostException(response.content)

                user['posts'].append(json.loads(response.content))

                rand_posts -= 1

    def like_posts(self, post_id, user):
        self.HEADERS['Authorization'] = 'Bearer '+ user['token']
        response = \
            requests.post(url='http://localhost:8000/api/posts/{}/like/'.format(post_id), headers=self.HEADERS)
        if not response.status_code == status.HTTP_201_CREATED:
            raise BotLikeException(response.content)

    def like_logic(self):
        posting_users = sorted(self.logged_users, key=lambda user: len(user['posts']))
        while True:
            max_posts_user = posting_users.pop()
            max_posts_user['posts_liked'] = []
            posts = self._get_posts(max_posts_user)
            if self._all_posts_liked(posts) or not posting_users:
                return print("Bot finished playing around! :)")

            while len(max_posts_user.get('posts_liked')) <= self.max_likes_per_user:
                random_post = random.choice(posts)
                if random_post['user'] != max_posts_user['user']['pk'] and \
                   random_post['id'] not in max_posts_user['posts_liked'] and \
                    self._no_likes_check(posts=posts, post_owner=random_post['user']):

                    self.like_posts(random_post['id'], max_posts_user)
                    max_posts_user['posts_liked'].append(random_post['id'])

            pass