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
        
        try:
            company = Company(
                alias="f",
                is_blocked=False,
                is_valid=True,
                settings=settings.COMPANY_SETTINGS
            )
            if company.full_clean() is None:
                company.save()
        except Exception as exc:
            raise CommandError("ERROR Company creation >> ", exc)

        self.stdout.write(self.style.SUCCESS(f"Successfully created a company with alias: {alias}"))
