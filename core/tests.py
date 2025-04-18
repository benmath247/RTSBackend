from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.factories import UserFactory, FavoriteStockFactory
from core.models import User, FavoriteStock
from unittest.mock import patch

class CurrentUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_current_user_authenticated(self):
        response = self.client.get(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_current_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_logout_authenticated_user(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')

class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('create_user'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

class EditUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_edit_user(self):
        payload = {'bio': 'Updated bio'}
        response = self.client.patch(reverse('edit_user'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'Updated bio')

class FavoriteStockCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_favorite_stock(self):
        user = UserFactory()
        payload = {'stock_symbol': 'AAPL', 'user': user.id}
        response = self.client.post(reverse('favorite-stock-create'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FavoriteStock.objects.filter(user=self.user, stock_symbol='AAPL').exists())

    def test_create_favorite_stock_unauthenticated(self):
        self.client.force_authenticate(user=None)
        payload = {'stock_symbol': 'AAPL'}
        response = self.client.post(reverse('favorite-stock-create'), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class FavoriteStockDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_delete_favorite_stock(self):
        favorite_stock = FavoriteStockFactory(user=self.user)
        response = self.client.delete(reverse('favorite-stock-delete', args=[favorite_stock.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteStock.objects.filter(id=favorite_stock.id).exists())

    def test_delete_favorite_stock_unauthenticated(self):
        favorite_stock = FavoriteStockFactory(user=self.user)
        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('favorite-stock-delete', args=[favorite_stock.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

