import uuid

from django.db import models

from appdata.models.abstract.audit_mixin import AModelAuditMixin


class IncidentTag(AModelAuditMixin):

    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, null=False, blank=False)


    class Meta:
        verbose_name = "Incident Tag"
        verbose_name_plural = "Incident Tags"
        db_table = "incident_tag"

    def __str__(self):
        return self.name
