import uuid

from django.db import models
from django.db.models import UniqueConstraint

from appdata.models.user import User
from appdata.models.incident import Incident
from appdata.models.abstract.audit_mixin import AModelAuditMixin


class IncidentVote(AModelAuditMixin):

    id = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4)
    incident = models.ForeignKey(to=Incident, on_delete=models.CASCADE, null=False, blank=False, related_name='votes')
    created_by_user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False, related_name='incident_votes')
    up_voted = models.BooleanField(null=False, blank=False)

    class Meta:
        verbose_name='Incident Vote'
        verbose_name_plural = "Incident Votes"
        db_table = 'incident_vote'
        constraints = [UniqueConstraint(fields=['incident', 'created_by_user'], name='unique_incident_vote')]


    def __str__(self):
        return f"Vote<{self.incident}, {self.up_voted}>"
