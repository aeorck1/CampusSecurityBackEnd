import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from appdata.managers import RoleManager
from appdata.models.abstract.audit_mixin import AModelAuditMixinNullableCreate


class Role(AModelAuditMixinNullableCreate):

    id = models.CharField(max_length=64, default=uuid.uuid4, primary_key=True)

    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    description = models.TextField(null=True, blank=True)

    objects = RoleManager()

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        db_table = 'role'

    def __str__(self):
        return f"Role<id={self.id}, name={self.name}>"

    def natural_key(self):
        return self.name
