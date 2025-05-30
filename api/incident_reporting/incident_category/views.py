from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from api.incident_reporting.incident_category.serializers import IncidentTagSerializer
from appdata.models import IncidentTag


@extend_schema_view(
    list=extend_schema(summary="List all incident tags", tags=['Incident Tag']),
    retrieve=extend_schema(summary="Retrieve a specific incident tag", tags=['Incident Tag'])
)
class IncidentTagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IncidentTag.objects.all()
    serializer_class = IncidentTagSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    create=extend_schema(summary="Create a new incident tag", tags=['Incident Tag']),
    update=extend_schema(summary="Update an incident tag", tags=['Incident Tag']),
    partial_update=extend_schema(summary="Partially update an incident tag", tags=['Incident Tag']),
    destroy=extend_schema(summary="Delete an incident tag", tags=['Incident Tag']),
    list=extend_schema(summary="List (write endpoint) incident tags", tags=['Incident Tag']),
    retrieve=extend_schema(summary="Retrieve (write endpoint) an incident tag", tags=['Incident Tag']),
)
class IncidentTagWriteViewSet(viewsets.ModelViewSet):
    queryset = IncidentTag.objects.all()
    serializer_class = IncidentTagSerializer
    permission_classes = [permissions.IsAdminUser]
