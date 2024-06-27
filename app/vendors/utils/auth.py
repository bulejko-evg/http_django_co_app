import logging
from app.vendors import messages as msg
from app.apps.account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.backends import ModelBackend


auth_logger = logging.getLogger("auth")


class AuthBackend(ModelBackend):
    """Custom account auth backend."""

    def authenticate(self, request, username=None, password=None, **kwargs) -> Account | None:
        user = self._get_user(username=username, password=password)
        if user is not None:
            auth_logger.info(f"{msg.USER_AUTHENTICATED}: {username}")
        return user

    def get_user(self, user_id) -> Account | None:
        user = self._get_user(pk=user_id)
        if user is not None:
            auth_logger.info(f"{msg.USER_GOT}: {user_id}")
        return user
    
    def _get_user(self, **get_parameres) -> Account | None:
        """Get account by get parameters, or None."""
        try:
            user = Account.objects.get(**get_parameres)
            get_parameres.pop("password", None) #  delete password from parameters
        except ObjectDoesNotExist:
            auth_logger.error(f"{msg.USER_IS_NOT_EXIST}: {get_parameres}")
            user = None
        else:
            is_actual, fail_messages = user.is_actual()
            if not is_actual:
                auth_logger.error(f"{msg.USER_IS_NOT_VALID}: {get_parameres}: {fail_messages}")
                user = None
        
        return user
