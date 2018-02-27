from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.models import SocialUser


class TestSocialViewSets(APITestCase):

    username = 'user'
    password = 'passwd'
    email = 'email@test.com'
    token = 0
    user_id = 0

    def setUp(self):
        url = reverse('signup_user')
        data = {'username': self.username,
                'email': self.email,
                'password': self.password}
        response = self.client.post(url, data, format='json')

        data = {'username': self.username,
                'password': self.password,
                'email': self.email,
                }
        url = reverse('token_auth')
        token_response = self.client.post(url, data, format='json')
        self.token = token_response.data['token']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SocialUser.objects.count(), 1)
        self.assertEqual(SocialUser.objects.get().username, self.username)
        self.assertEqual(SocialUser.objects.get().email, self.email)


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
        response = self.client.get(url, Authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    # def test_create_post(self):
    #     pass
    #