from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.factories import UserFactory, FavoriteStockFactory
from core.models import User, FavoriteStock
from core.serializers import FavoriteStockSerializer


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


class FavoriteStockSerializerTest(TestCase):
    def test_favorite_stock_serializer(self):
        user = UserFactory()
        favorite_stock = FavoriteStockFactory(user=user)
        serializer = FavoriteStockSerializer(favorite_stock)
        self.assertEqual(serializer.data["stock_symbol"], favorite_stock.stock_symbol)
        self.assertEqual(serializer.data["user"], user.id)


class FavoriteStockFactoryTest(TestCase):
    def test_favorite_stock_factory(self):
        favorite_stock = FavoriteStockFactory()
        self.assertIsInstance(favorite_stock, FavoriteStock)
        self.assertIsNotNone(favorite_stock.user)
        self.assertIsNotNone(favorite_stock.stock_symbol)


class FavoriteStockListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.favorite_stock = FavoriteStockFactory(user=self.user)

    def test_get_favorite_stocks(self):
        response = self.client.get(reverse("favorite-stock-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["stock_symbol"],
            self.favorite_stock.stock_symbol,
        )

    def test_get_favorite_stocks_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("favorite-stock-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FavoriteStockCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_favorite_stock(self):
        payload = {
            "stock_symbol": "AAPL",
            "user": self.user.id,
        }
        response = self.client.post(reverse("favorite-stock-create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FavoriteStock.objects.filter(stock_symbol="AAPL", user=self.user).exists()
        )

    def test_create_favorite_stock_unauthenticated(self):
        self.client.force_authenticate(user=None)
        payload = {"stock_symbol": "AAPL"}
        response = self.client.post(reverse("favorite-stock-create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FavoriteStockDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.favorite_stock = FavoriteStockFactory(user=self.user)

    def test_delete_favorite_stock_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse("favorite-stock-delete", args=[self.favorite_stock.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_favorite_stock_not_found(self):
        response = self.client.delete(reverse("favorite-stock-delete", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_favorite_stock_not_owned(self):
        other_user = UserFactory()
        other_favorite_stock = FavoriteStockFactory(user=other_user)
        response = self.client.delete(
            reverse("favorite-stock-delete", args=[other_favorite_stock.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_favorite_stock_invalid_id(self):
        response = self.client.delete(reverse("favorite-stock-delete", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_favorite_stock_no_id(self):
        response = self.client.delete(reverse("favorite-stock-delete", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_favorite_stock_no_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse("favorite-stock-delete", args=[self.favorite_stock.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
