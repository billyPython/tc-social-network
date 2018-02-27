from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.models import SocialUser, Post


class TestSocialViewSets(APITestCase):

    username = 'user'
    password = 'passwd'
    email = 'email@test.com'
    token = 0
    user_id = 0

    def setUp(self):

        self.user = SocialUser.objects.create_user(username="sejoo", email="kalac@test.com", password="mooo1345")
        #Create post se we can test like view
        self.post = Post.objects.create(title="Test post title", text="test test test", user=self.user)

        data = {
            'username': self.user.username,
            'password': 'mooo1345',
        }
        url = reverse('token_auth')
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup(self):
        # Signup
        url = reverse('signup_user')
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SocialUser.objects.get(username=data['username']).username, self.username)
        self.assertEqual(SocialUser.objects.get(email=data['email']).email, self.email)

    def test_invalid_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('signup_user')
        data = {'email':'nick@test.com', 'password': 'top_secret'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list_view(self):
        url = reverse('api:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        url = reverse('api:posts-list')
        data = {
            "title": "Test post title 2",
            "text": "test2 test2 test2",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.get(id=response.data['id']).title, data['title'])
        self.assertEqual(Post.objects.get(id=response.data['id']).text, data['text'])

    def test_create_invalid_post(self):
        url = reverse('api:posts-list')
        data = {
            "text": "test test test",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_post(self):
        url = '/api/posts/{}/like/'.format(self.post.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.get(pk=self.post.pk).liked, 1)