
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from core.utils.enum import Enum


class DefaultRoles(Enum):
    SYSTEM_ADMIN = 'System Admin'
    STUDENT = 'Student'
    ADMIN = 'Admin'


class RoleManager(models.Manager):
    """Role manager
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class UserManager(BaseUserManager):

    def _create_user(self, email, username, role_id, password, **extra_fields):
        """Create and save a user with the given email, username and password
        """

        if not email:
            raise ValueError("The given email must be set")

        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, role_id=role_id, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_system_admin(self, email, username, password, **extra_fields):
        user = self._create_user(email=email,
                                 username=username,
                                 role_id=DefaultRoles.SYSTEM_ADMIN.name,
                                 password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, role, password, **extra_fields):
        return self._create_user(email=email,
                                 username=username,
                                 role_id=role.id,
                                 password=password,
                                 **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_system_admin(email=email, username=username, password=password, **extra_fields)
