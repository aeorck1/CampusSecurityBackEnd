import uuid

from django.db import models
from django.db.models import UniqueConstraint

from appdata.models.user import User
from appdata.models.abstract.audit_mixin import AModelAuditDateMixin
from core.constants.system_enums import ObjectType


class CommentParticipant(AModelAuditDateMixin):
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4())

    object_type = models.CharField(max_length=64, choices=ObjectType.mapping(), null=False, blank=False)
    object_id = models.CharField(max_length=64, null=False, blank=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)
    last_count = models.BigIntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Comment Participant'
        verbose_name_plural = 'Comment Participants'
        db_table = 'comment_participant'
        constraints = [
            UniqueConstraint(fields=['user', 'object_id', 'object_type'], name='unique_participant_user_id_object_id'),
        ]

    def __str__(self):
        return f"CommentParticipant<object_type='{self.object_type}' object_id={self.object_id} last_count='{self.last_count}', user='{self.user}'>"
