import pytest
from faker import Faker
from django.conf import settings
from app.apps.account import models
from app.vendors.helpers import generate_password
from .factories import (
    AccountFactory,
    AdminFactory,
    EmployeeFactory,
    CustomerFactory,
    GuestFactory,
    ProfileFactory,
)


fake = Faker(settings.LANGUAGES_CODES)


MIDDLE_NAME = ["", "Middle"]


@pytest.mark.models
@pytest.mark.django_db
def test_account_create():
    username = fake.lexify(text="??????")
    account = AccountFactory(username=username)

    try:
        account._permissions = {"access": "access"}
        is_permissions_change = True
    except AttributeError:
        is_permissions_change = False

    assert account.full_clean() is None, "Save model error"
    assert account.username == username, "Incorrect username after save"
    assert is_permissions_change is False, "Immutable _permissions has changed"


@pytest.mark.models
@pytest.mark.django_db
def test_account_create_user_method():
    username = fake.lexify(text="??????")
    password = generate_password()

    account = models.Account.objects.create_user(
        username=username,
        email="mail@mail.com",
        password=password,
    )
    assert account.full_clean() is None, "Save model error"
    assert account.username == username, "Incorrect username after save"


@pytest.mark.models
@pytest.mark.django_db
def test_admin_create():
    username = fake.lexify(text="??????")
    adm = AdminFactory(username=username)
    assert adm.full_clean() is None, "Save model error"
    assert adm.save(set_permissions=True) is None, "Save model with permissions error"
    adm.confirmed = True

    assert adm.has_perm("account.view_dashboard") is True, "Permission view_dashboard not added"
    assert adm.username == username, "Incorrect username after save"
    assert adm.is_confirmed is True, "Confirm is false"
    assert adm.is_blocked is False, "Blocked is true"
    assert adm.is_valid is True, "Valid is false"


@pytest.mark.models
@pytest.mark.django_db
def test_employee_create():
    username = fake.lexify(text="??????")
    employee = EmployeeFactory(username=username)
    assert employee.full_clean() is None, "Save model error"
    assert employee.save(set_permissions=True) is None, "Save model with permissions error"
    employee.confirmed = True

    assert employee.has_perm("account.view_dashboard") is True, "Permission view_dashboard not added"
    assert employee.username == username, "Incorrect username after save"
    assert employee.is_confirmed is True, "Confirm is false"
    assert employee.is_blocked is False, "Blocked is true"
    assert employee.is_valid is True, "Valid is false"


@pytest.mark.models
@pytest.mark.django_db
def test_customer_create():
    username = fake.lexify(text="??????")
    customer = CustomerFactory(username=username)
    assert customer.full_clean() is None, "Save model error"
    assert customer.save(set_permissions=True) is None, "Save model with permissions error"
    customer.confirmed = True

    assert customer.has_perm("account.view_dashboard") is True, "Permission view_dashboard not added"
    assert customer.username == username, "Incorrect username after save"
    assert customer.is_confirmed is True, "Confirm is false"
    assert customer.is_blocked is False, "Blocked is true"
    assert customer.is_valid is True, "Valid is false"


@pytest.mark.models
@pytest.mark.django_db
def test_guest_create():
    username = fake.lexify(text="??????")
    guest = GuestFactory(username=username)
    assert guest.full_clean() is None, "Save model error"
    guest.confirmed = True

    assert guest.has_perm("account.view_dashboard") is False, "Permission view_dashboard added for guest role"
    assert guest.username == username, "Incorrect username after save"
    assert guest.is_confirmed is True, "Confirm is false"
    assert guest.is_blocked is False, "Blocked is true"
    assert guest.is_valid is True, "Valid is false"


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize("middle_name", MIDDLE_NAME)
def test_profile_create(middle_name, image_file_png):
    profile = ProfileFactory(middle_name=middle_name)
    profile.photo = image_file_png

    assert profile.full_clean() is None, "Save model error"


@pytest.mark.models
@pytest.mark.django_db
def test_account_update():
    account = AccountFactory()

    assert account.full_clean() is None, "Save model error"

    account = models.Account.objects.get(pk=account.id)
    username = fake.lexify(text="??????")
    account.username = username
    account.email = f"{username}@mail.com"
    account.is_staff = False
    account.is_active = True

    assert account.full_clean() is None, "Update model error"


@pytest.mark.models
@pytest.mark.django_db
def test_profile_update():
    profile = ProfileFactory()

    assert profile.full_clean() is None, "Save model error"

    profile.first_name = fake.first_name()
    profile.middle_name = fake.first_name()
    profile.last_name = fake.last_name()
    profile.age = 22
    profile.birthdate = fake.date()
    profile.gender = models.Profile.Gender.MALE

    assert profile.full_clean() is None, "Update model error"


@pytest.mark.models
@pytest.mark.django_db
def test_account_profile_soft_delete():
    account = AccountFactory()
    ProfileFactory(account=account)
    account_id = account.id
    account.delete(soft=True)

    is_account_exist = models.Account.objects.filter(
        id=account_id, 
        deleted_at__isnull=False
    ).exists()
    is_profile_exist = models.Profile.objects.filter(account_id=account_id).exists()

    assert is_account_exist is True, "Account is not exist after soft deleted"
    assert is_profile_exist is True, "Profile is not exist after soft deleted"


@pytest.mark.models
@pytest.mark.django_db
def test_account_profile_delete():
    account = AccountFactory()
    ProfileFactory(account=account)
    account_id = account.id
    account.delete()

    is_account_exist = models.Account.objects.filter(id=account_id).exists()
    is_profile_exist = models.Profile.objects.filter(account_id=account_id).exists()

    assert is_account_exist is False, "Account exist after deleted"
    assert is_profile_exist is False, "Profile exist after deleted"
