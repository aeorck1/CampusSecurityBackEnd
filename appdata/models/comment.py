import uuid

from django.db import models

from appdata.models.user import User
from appdata.models.abstract.audit_mixin import AModelAuditMixin
from core.constants.system_enums import ObjectType


class Comment(AModelAuditMixin):
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    object_id = models.CharField(max_length=64, null=False, blank=False)
    parent_comment = models.ForeignKey(to='self', max_length=64, null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    comment = models.TextField(null=True, blank=True)
    object_type = models.CharField(max_length=64, choices=ObjectType.mapping(), null=False, blank=False)
    parent_comment_metadata = models.JSONField(null=True, blank=True)
    position = models.BigIntegerField(null=False, blank=False)
    comment_by = models.ForeignKey(User, to_field='id', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'comment'

    def __str__(self):
        return f"Comment(id='{self.id}', object_id='{self.object_id}', comment='{self.comment}', object_type='{self.object_type}')"
