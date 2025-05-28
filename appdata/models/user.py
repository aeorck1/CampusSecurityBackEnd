import os
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from appdata.managers import UserManager


def upload_avatar(instance, filename):
    path = os.path.join(settings.USER_ACCOUNT_FILES_DIR_ROOT, 'avatar', filename)
    return path


class User(AbstractBaseUser, PermissionsMixin):

    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)

    email = models.EmailField(verbose_name=_("Email Address"),
                              unique=True,
                              max_length=255,
                              validators=[EmailValidator()])

    username = models.CharField(max_length=64, unique=True, null=False, blank=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    first_name = models.CharField(max_length=64)

    last_name = models.CharField(max_length=64)

    middle_name = models.CharField(max_length=64)

    role = models.ForeignKey(to="Role",
                             verbose_name=_('role'),
                             blank=True,
                             help_text=_(
                                 'The role this user belongs to. A user will get all permissions '
                                 'granted to their role.'),
                             related_name="user_set",
                             on_delete=models.RESTRICT)

    profile_picture = models.ImageField(upload_to=upload_avatar,
                                        null=True,
                                        blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')
        db_table = 'campus_security_user'

    def __str__(self):
        return f"CampusSecurityUser<{self.email}>"
