import factory
from django.contrib.auth.hashers import make_password
from core.models import User, FavoriteStock


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    bio = factory.Faker("text", max_nb_chars=500)
    birth_date = factory.Faker("date_of_birth")
    profile_picture = None
    password = factory.LazyFunction(lambda: make_password("password123"))


class FavoriteStockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteStock

    user = factory.SubFactory(UserFactory)
    stock_symbol = factory.Faker("bothify", text="??????")
