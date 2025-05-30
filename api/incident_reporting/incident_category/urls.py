from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.incident_reporting.incident_category.views import IncidentTagReadOnlyViewSet, IncidentTagWriteViewSet

router = DefaultRouter()
router.register(r'', IncidentTagReadOnlyViewSet, basename='incident-category-read')
router.register(r'admin', IncidentTagWriteViewSet, basename='incident-category-manage')
# router.register(r'incidents', IncidentViewSet, basename='incident')

urlpatterns = [
    path('', include(router.urls)),
]
