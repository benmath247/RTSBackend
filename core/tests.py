from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.factories import UserFactory
from core.models import User


class CurrentUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_current_user_authenticated(self):
        response = self.client.get(reverse("current_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_current_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("current_user"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_logout_authenticated_user(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        }
        response = self.client.post(reverse("create_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())


class EditUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_edit_user(self):
        payload = {"bio": "Updated bio"}
        response = self.client.patch(reverse("edit_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Updated bio")


class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(reverse("create_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_register_user_duplicate_email(self):
        UserFactory(email="duplicate@example.com")
        payload = {
            "username": "newuser",
            "email": "duplicate@example.com",
            "password": "password123",
        }
        response = self.client.post(reverse("create_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already exists", str(response.data))


class EditUserDetailsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_edit_user_details_success(self):
        payload = {"bio": "Updated bio", "birth_date": "1990/01/01"}
        response = self.client.patch(reverse("edit_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Updated bio")
        self.assertEqual(self.user.birth_date.strftime("%Y/%m/%d"), "1990/01/01")

    def test_edit_user_details_unauthenticated(self):
        self.client.force_authenticate(user=None)
        payload = {"bio": "Updated bio"}
        response = self.client.patch(reverse("edit_user"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# finnhub disabled my account when I run these tests

# class StockPriceViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_get_stock_price_success(self):
#         ticker = 'AAPL'
#         response = self.client.get(reverse('stock_data'), {'ticker': ticker})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('c', response.data)
#         self.assertIn('d', response.data)
#         self.assertIn('dp', response.data)
#         self.assertIn('h', response.data)
#         self.assertIn('o', response.data)
#         self.assertIn('pc', response.data)
#         self.assertIn('t', response.data)


#     def test_get_stock_price_missing_ticker(self):
#         response = self.client.get(reverse('stock_data'))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('Ticker is required', str(response.data))
