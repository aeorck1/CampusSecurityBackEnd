import uuid

from django.db import models

from appdata.models.comment import Comment
from appdata.models.abstract.audit_mixin import AModelAuditMixinNullableCreate
from appdata.models.incident_category import IncidentTag
from appdata.models.user import User
from core.constants.system_enums import ObjectType
from core.utils.enum import Enum


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"



class IncidentStatus(Enum):
    ACTIVE = "ACTIVE"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"


class Incident(AModelAuditMixinNullableCreate):

    id = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, blank=True)
    title = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    severity = models.CharField(max_length=32, null=False, blank=False, choices=Severity.mapping())
    location = models.CharField(max_length=256, null=False, blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tags = models.ManyToManyField(IncidentTag, related_name="incidents")
    status = models.CharField(max_length=32, choices=IncidentStatus.mapping(), default=IncidentStatus.ACTIVE, null=False, blank=True)
    created_by_user = models.ForeignKey(User, related_name="incidents", on_delete=models.SET_NULL, null=True, blank=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    reporter_satisfaction = models.FloatField(null=True, blank=True) # Satisfaction level in percentage between 0 and 1

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        db_table = "incident"

    def __str__(self):
        return self.title

    @property
    def reported_by(self):
        return self.created_by_user

    @property
    def comments(self):
        return Comment.objects.filter(
            object_id=self.id,
            object_type=ObjectType.INCIDENT.name
        ).order_by('position')

    @property
    def up_votes(self):
        return  self.votes.filter(up_voted=True).count()

    @property
    def down_votes(self):
        return self.votes.filter(up_voted=False).count()