from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(APITestCase):

    def test_register(self):
        response = self.client.post(
            '/api/register/',
            {
                'username': 'testuser',
                'email': 'test@gmail.com',
                'password': 'StrongPass123!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        self.client.post(
            '/api/register/',
            {
                'username': 'testuser',
                'email': 'test@gmail.com',
                'password': 'StrongPass123!'
            }
        )

        response = self.client.post(
            '/api/login/',
            {
                'username': 'testuser',
                'password': 'StrongPass123!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile(self):
        self.client.post(
            '/api/register/',
            {
                'username': 'testuser',
                'email': 'test@gmail.com',
                'password': 'StrongPass123!'
            }
        )

        response = self.client.post(
            '/api/login/',
            {
                'username': 'testuser',
                'password': 'StrongPass123!'
            }
        )

        token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)