import factory
from faker import Faker
from django.conf import settings
from app.apps.company import models


fake = Faker(settings.LANGUAGES_CODES)


class CompanyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Company

    alias = fake.lexify(text="????")
    names = {settings.LANGUAGE_CODE: fake.lexify(text="??????")}
    descriptions = {settings.LANGUAGE_CODE: fake.paragraph(nb_sentences=2)}
    settings = settings.COMPANY_SETTINGS


class CompanyTranslateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.CompanyTranslate

    rich_text = fake.paragraph(nb_sentences=10)
    company = factory.SubFactory(CompanyFactory)
