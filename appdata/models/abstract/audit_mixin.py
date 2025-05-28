from django.db import models
from django.utils.translation import gettext_lazy as _

from appdata.model_util import jsonify_user
from appdata.models.user import User
from campus_security_api.middlewares.context_user import get_context_user


class AModelAuditDateMixin(models.Model):
    """
        This mixin provides auditing on models (timestamp of operation)

        Attributes:
            date_created (DateTime): Date when new record was inserted into a table
            date_last_modified (DateTime): Date when record was last modified
    """
    date_created = models.DateTimeField(verbose_name=_('Date Created'), auto_now_add=True)
    date_last_modified = models.DateTimeField(verbose_name=_('Date Last Modified'), auto_now=True)

    class Meta:
        abstract = True


class AModelAuditMixin(AModelAuditDateMixin):
    """
    This mixin provides auditing on models

    Attributes:
        date_created (DateTime): Date when new record was inserted into a table
        created_by_user (json): User responsible for inserting the record
        date_last_modified (DateTime): Date when record was last modified
        last_modified_by_user (json): User responsible for the last modification of the record
    """

    created_by_user = models.JSONField(verbose_name=_('Created by user'), null=False, blank=True)
    last_modified_by_user = models.JSONField(verbose_name=_('Last modified by user'), null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def created_by(self):
        if self.created_by_user:
            return User.objects.get(pk=self.created_by_user.get('id'))
        return None

    @property
    def last_modified_by(self):
        if self.last_modified_by_user:
            return User.objects.get(pk=self.last_modified_by_user.get('id'))
        return None

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):

        if self._state.adding:  # New instance
            if self.created_by_user is None:
                context_user_json = jsonify_user(get_context_user())
                self.created_by_user = context_user_json
        else:
            if self.last_modified_by_user is None:
                context_user_json = jsonify_user(get_context_user())
                self.last_modified_by_user = context_user_json

        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)


class AModelAuditMixinNullableCreate(AModelAuditMixin):
    """
        This mixin provides auditing on models (The created_by field can be null)

        Attributes:
            date_created (DateTime): Date when new record was inserted into a table
            created_by_user (json): User responsible for inserting the record
            date_last_modified (DateTime): Date when record was last modified
            last_modified_by_user (json): User responsible for the last modification of the record
    """
    created_by_user = models.JSONField(verbose_name=_('Created by user ID'), null=True, blank=True)

    class Meta:
        abstract = True


    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):

        if self._state.adding:  # New instance
            pass
        else:
            if self.last_modified_by_user is None:
                context_user_json = jsonify_user(get_context_user())
                self.last_modified_by_user = context_user_json

        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)
