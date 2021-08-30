from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'username': 'username',
            'password': 'test_password'
        }
        cls.domain = 'http://127.0.0.1:8000'
        cls.create_user_url = f'{cls.domain}/api/auth/users/'
        cls.get_token_url = f'{cls.domain}/api/auth/token/login/'

    def test_create_account(self):
        response = self.client.post(
            self.create_user_url,
            self.data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'username')

    def test_get_token(self):
        self.client.post(self.create_user_url, self.data, format='json')
        response = self.client.post(
            self.get_token_url,
            self.data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.json())
