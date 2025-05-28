from django.db.models import ExpressionWrapper, F, DurationField, Avg
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.incident_reporting.incident.serializers import IncidentCreateSerializer, IncidentSerializer, \
    IncidentStatusUpdateSerializer, IncidentStatisticsSerializer, IncidentSatisfactionSerializer
from appdata.models.incident import Incident


# Custom permission
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# Anyone can create (anonymous)
@extend_schema_view(
    create=extend_schema(summary="Report incident anonymously", tags=['Incident'])
)
class IncidentAnonymousCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentCreateSerializer
    permission_classes = [permissions.AllowAny]

# Authenticated create
@extend_schema_view(
    create=extend_schema(summary="Report incident as authenticated user", tags=['Incident'])
)
class IncidentAuthCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

# Admin read/update/delete
@extend_schema_view(
    list=extend_schema(summary="List incidents (admin only)", tags=['Incident']),
    retrieve=extend_schema(summary="Retrieve incident (admin only)", tags=['Incident']),
    update=extend_schema(summary="Update incident", tags=['Incident']),
    partial_update=extend_schema(summary="Partially update incident", tags=['Incident']),
    destroy=extend_schema(summary="Delete incident", tags=['Incident'])
)
class IncidentAdminViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ('get', 'put', 'patch', 'delete')


@extend_schema_view(
    get=extend_schema(summary="List incidents (public)", tags=['Incident']),
)
class IncidentPublicRetrieveViewSet(RetrieveAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.AllowAny]

# Update status
@extend_schema_view(
    partial_update=extend_schema(
        summary="Update incident status",
        parameters=[
            OpenApiParameter("id", str, OpenApiParameter.PATH, description="Incident ID")
        ],
        tags=['Incident']
    )
)
class IncidentStatusUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


@extend_schema(
    summary="Incident Statistics",
    description="Returns incident statistics including total counts, average response time, and average satisfaction.",
    tags=['Incident'],
    responses={200: IncidentStatisticsSerializer}
)
class IncidentStatisticsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_incidents = Incident.objects.count()
        active_incidents = Incident.objects.filter(status='ACTIVE').count()
        resolved_incidents = Incident.objects.filter(status='RESOLVED').count()
        investigating_incidents = Incident.objects.filter(status='INVESTIGATING').count()

        # Average response time
        response_times = Incident.objects.filter(
            status='RESOLVED',
            date_resolved__isnull=False,
            created_at__isnull=False  # assuming AModelAuditMixinNullableCreate has created_at
        ).annotate(
            response_duration=ExpressionWrapper(
                F('date_resolved') - F('date_created'),
                output_field=DurationField()
            )
        ).aggregate(avg_response_time=Avg('response_duration'))

        avg_duration = response_times['avg_response_time']

        # Determine appropriate unit
        if avg_duration:
            total_seconds = avg_duration.total_seconds()
            if total_seconds < 3600:
                value = total_seconds / 60
                unit = "minutes"
            elif total_seconds < 86400:
                value = total_seconds / 3600
                unit = "hours"
            else:
                value = total_seconds / 86400
                unit = "days"
            average_response_time = f"{round(value, 2)} {unit}"
        else:
            average_response_time = "N/A"

        # Average satisfaction (only for resolved incidents with non-null satisfaction)
        avg_satisfaction = Incident.objects.filter(
            status='RESOLVED',
            reporter_satisfaction__isnull=False
        ).aggregate(avg_satisfaction=Avg('reporter_satisfaction'))['avg_satisfaction']

        data = {
            'total_incidents': total_incidents,
            'active_incidents': active_incidents,
            'resolved_incidents': resolved_incidents,
            'investigating_incidents': investigating_incidents,
            'average_response_time': average_response_time,
            'average_satisfaction': round(avg_satisfaction, 2) if avg_satisfaction is not None else None
        }

        serializer = IncidentStatisticsSerializer(data)
        return Response(serializer.data)


@extend_schema(
    summary="Submit satisfaction level for an incident",
    description="Allows the reporter of an incident to submit their satisfaction level (0 to 1) after it is resolved.",
    tags=['Incident']
)
class IncidentSatisfactionView(generics.UpdateAPIView):
    serializer_class = IncidentSatisfactionSerializer
    queryset = Incident.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ('patch', )

    def get_object(self):
        incident = super().get_object()
        user = self.request.user
        if incident.created_by_user != user:
            raise PermissionDenied("You can only submit satisfaction for incidents you reported.")
        if incident.status != 'RESOLVED':
            raise ValidationError("You can only submit satisfaction for resolved incidents.")
        return incident


@extend_schema(
    summary="Fetch incidents reported by the authenticated user",
    description="Returns a list of incidents that the signed-in user has reported.",
    tags=['Incident']
)
class UserIncidentsListView(generics.ListAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(created_by_user=self.request.user)
