from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.incident_reporting.incident.views import IncidentAnonymousCreateViewSet, IncidentAuthCreateViewSet, \
    IncidentAdminViewSet, IncidentStatusUpdateViewSet, IncidentStatisticsView, IncidentSatisfactionView, \
    UserIncidentsListView

router = DefaultRouter()
router.register('anonymous/incidents', IncidentAnonymousCreateViewSet, basename='incident-anon-create')
router.register('incidents', IncidentAuthCreateViewSet, basename='incident-auth-create')
router.register('admin/incidents', IncidentAdminViewSet, basename='incident-admin')
# router.register('admin/resolution/incidents', IncidentStatusUpdateViewSet, basename='incident-status')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/incidents/<str:id>/status/', IncidentStatusUpdateViewSet.as_view({"patch": "partial_update"}), name='incident-status'),
    path('admin/incident-statistics/', IncidentStatisticsView.as_view(), name='incident-statistics'),
    path('incidents/<str:pk>/satisfaction/', IncidentSatisfactionView.as_view(), name='incident-satisfaction'),
    path('incidents/my-reports/', UserIncidentsListView.as_view(), name='my-reported-incidents'),
]
