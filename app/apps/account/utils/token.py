from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountTokenGenerator(PasswordResetTokenGenerator):
    """Generate unique hash for account"""

    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )


account_token = AccountTokenGenerator()