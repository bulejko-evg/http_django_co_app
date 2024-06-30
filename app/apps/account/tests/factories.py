import factory
from faker import Faker
from django.conf import settings
from app.apps.account import models
from factory.fuzzy import FuzzyChoice


fake = Faker(settings.LANGUAGES_CODES)


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Account

    username = fake.lexify(text="??????")
    email = factory.Sequence(lambda n: f"mail_{n}@mail.com")
    password = "!Q2w3e4r5t"
    is_staff = False
    is_active = True


class AdminFactory(AccountFactory):

    class Meta:
        model = models.Admin


class EmployeeFactory(AccountFactory):

    class Meta:
        model = models.Employee


class CustomerFactory(AccountFactory):

    class Meta:
        model = models.Customer


class GuestFactory(AccountFactory):

    class Meta:
        model = models.Guest


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Profile

    account = factory.SubFactory(AccountFactory)
    first_name = fake.first_name()
    last_name = fake.last_name()
    age = 99
    birthdate = fake.date()
    gender = FuzzyChoice(choices=["FEMALE", "MALE"])
