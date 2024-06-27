from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def set_account_permissions(account, models_roles_permissions: dict) -> None:
    """
    Set permissions for account.
    -----------------------------
    Parameters:
        account (Account): current account
        models_roles_permissions (dict): dict of permissions for model by roles,
            dict of dicts from method get_permission from mixin RolePermissionsMixin.
    Returns:
        _
    """
    account.user_permissions.clear()
    all_permissions = {**account.get_permissions(), **models_roles_permissions}
    for app_model, perms in all_permissions.items():
        account_role = str(account.role).lower()
        app, model = app_model.split(":")
        content_type = ContentType.objects.get(app_label=app, model=model)

        if model_perms := perms.get(account_role, None):
            cont_type_perms = Permission.objects.filter(content_type=content_type)

            if isinstance(model_perms, str) and model_perms == "__all__":
                perms_ids = [p.id for p in cont_type_perms]
            elif isinstance(model_perms, list):
                perms_ids = [p.id for p in cont_type_perms if p.codename in model_perms]
            else:
                perms_ids = []
            account.user_permissions.add(*perms_ids)


