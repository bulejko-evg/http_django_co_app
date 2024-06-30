from django.conf import settings
from app.apps.company.models import Company


def get_company_ctx_data(**kwargs: any) -> Company | dict:
    """
    Get Company instance from db or cache.
    (If it is not exist return default company obj with default settings).
    """
    company = Company.get_from_cache(prefix=settings.COMPANY_ALIAS, alias=settings.COMPANY_ALIAS)
    if company is None:
        # Default data of company
        company = Company(
            id=1,
            alias=settings.COMPANY_ALIAS,
            settings=settings.COMPANY_SETTINGS,
        )
    return company