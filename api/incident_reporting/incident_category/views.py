from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from api.incident_reporting.incident_category.serializers import IncidentCategorySerializer
from appdata.models import IncidentCategory


@extend_schema_view(
    list=extend_schema(summary="List all incident categories", tags=['Incident Category']),
    retrieve=extend_schema(summary="Retrieve a specific incident category", tags=['Incident Category'])
)
class IncidentCategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IncidentCategory.objects.all()
    serializer_class = IncidentCategorySerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    create=extend_schema(summary="Create a new incident category", tags=['Incident Category']),
    update=extend_schema(summary="Update an incident category", tags=['Incident Category']),
    partial_update=extend_schema(summary="Partially update an incident category", tags=['Incident Category']),
    destroy=extend_schema(summary="Delete an incident category", tags=['Incident Category']),
    list=extend_schema(summary="List (write endpoint) incident categories", tags=['Incident Category']),
    retrieve=extend_schema(summary="Retrieve (write endpoint) an incident category", tags=['Incident Category']),
)
class IncidentCategoryWriteViewSet(viewsets.ModelViewSet):
    queryset = IncidentCategory.objects.all()
    serializer_class = IncidentCategorySerializer
    permission_classes = [permissions.IsAdminUser]
