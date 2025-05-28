from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied

from api.system_administration.user.services import UserService


class UsernameEmailBackend(BaseBackend):
    """
    Authenticate against the user email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = self.get_user(username)
        if user is not None:
            if not user.is_active:
                raise PermissionDenied("Account is inactive")
            if user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        try:
            return UserService.get_user_by_email_or_username(user_id)
        except UserService.model.DoesNotExist:
            return None
