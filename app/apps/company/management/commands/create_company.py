from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from app.apps.company.models import Company


class Command(BaseCommand):
    """
    Command for create company.
    Settings for company - settings.COMPANY_DEFAULT_SETTINGS
    Arguments:
        --alias: unique alias for company, optional, default value from settings.COMPANY_ALIAS
    """
    help = "Create Company with alias"

    def add_arguments(self, parser):
        parser.add_argument("--alias", type=str, help="unique alias of company")

    def handle(self, *args, **options):
        alias = options.get("alias")

        if not alias:
            try:
                alias = settings.COMPANY_ALIAS
            except AttributeError:
                raise CommandError("set --alias=<company_alias>, or set settings.COMPANY_ALIAS value")
        
        company = Company.objects.filter(alias=alias).first()
        if company is not None:
            raise CommandError(f"A company with the same alias ({alias}) already exists")
        
        ompany = Company.objects.create()
        # try:
        #     company = Company.objects.create(
        #         alias=alias,
        #         is_blocked=False,
        #         is_valid=True,
        #         settings=settings.COMPANY_SETTINGS
        #     )
        #     company.save()
        # except Exception as e:
        #     raise CommandError("ERROR Company creation >> ", e)

        self.stdout.write(self.style.SUCCESS(f"Successfully created a company with alias: {alias}"))
