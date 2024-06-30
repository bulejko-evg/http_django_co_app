import pytest
from faker import Faker
from django.conf import settings
from app.apps.company import models
from .factories import (
    CompanyFactory,
    CompanyTranslateFactory,
)


fake = Faker(settings.LANGUAGES_CODES)


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize("lang_key", settings.LANGUAGES_CODES)
def test_company_create(lang_key, image_file_ico, image_file_jpg, image_file_png):
    names = {lang_key: fake.lexify(text="??????")}
    company = CompanyFactory(
        names=names,
    )
    company.icon = image_file_ico
    company.logo = image_file_jpg
    company.banner = image_file_png

    assert company.full_clean() is None, "Save company error"
    assert company.names == names, "Names company error"


@pytest.mark.models
@pytest.mark.django_db
def test_company_update():
    company = CompanyFactory()

    assert company.full_clean() is None, "Save company error"

    company = models.Company.objects.get(pk=company.id)

    company.alias = fake.lexify(text="?????")
    company.names = {settings.LANGUAGE_CODE: fake.lexify(text="??????")}
    company.descriptions = {settings.LANGUAGE_CODE: fake.paragraph(nb_sentences=2)}
    company.settings = settings.COMPANY_SETTINGS

    assert company.full_clean() is None, "Update company error"


@pytest.mark.models
@pytest.mark.django_db
def test_company_delete():
    company = CompanyFactory()
    company_id = company.id
    company.delete()

    is_company_exist = models.Company.objects.filter(id=company_id).exists()

    assert is_company_exist is False, "Delete company error"


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize("lang_key", settings.LANGUAGES_CODES)
def test_company_translate_create(lang_key):
    company = CompanyFactory()

    company_translate = CompanyTranslateFactory(
        company=company,
        lang=lang_key,
        rich_text=fake.paragraph(nb_sentences=10)
    )
    assert company_translate.full_clean() is None, "Save company translate error"


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize("lang_key", settings.LANGUAGES_CODES)
def test_company_translate_update(lang_key):
    company_translate = CompanyTranslateFactory(
        lang=lang_key,
    )
    assert company_translate.full_clean() is None, "Save company translate error"

    company_translate.rich_text = fake.paragraph(nb_sentences=10)

    assert company_translate.full_clean() is None, "Update company translate error"


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize("lang_key", settings.LANGUAGES_CODES)
def test_company_translate_delete(lang_key):
    company = CompanyFactory()
    company_id = company.id
    CompanyTranslateFactory(
        company=company,
        lang=lang_key,
    )
    company.delete()

    is_company_exist = models.Company.objects.filter(id=company_id).exists()
    is_company_translate_exist = models.CompanyTranslate.objects.filter(
        company_id=company_id
    ).exists()

    assert is_company_exist is False, "Delete company error"
    assert is_company_translate_exist is False, "Delete company translate error"
