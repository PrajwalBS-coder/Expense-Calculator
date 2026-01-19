from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models.user_management import User

class CreateUserTest(APITestCase):
    def test_create_user(self):
        url = reverse('user-create')
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_create_user_invalid_data(self):
        url = reverse('user-create')
        data = {
            'email': 'invalid-email',
            'password': '123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
