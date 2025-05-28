from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q

from core.api.exceptions.exc import ResourceNotFoundException


class UserService:

    model = get_user_model()

    @classmethod
    def get_user_by_email_or_username(cls, email_or_username: str, raise_exception=True) -> AbstractBaseUser | None:
        try:
            return cls.model.objects.get(Q(username=email_or_username) | Q(email=email_or_username))
        except cls.model.DoesNotExist:
            if raise_exception:
                raise ResourceNotFoundException("User not found.")

    @classmethod
    def get_user(cls, user_id: str) -> model:
        try:
            return cls.model.objects.get(id=user_id)
        except cls.model.DoesNotExist:
            raise ResourceNotFoundException("User not found.")

    @classmethod
    def get_users(cls):
        return cls.model.objects.all()

