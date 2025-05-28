from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.incident_reporting.incident_category.views import IncidentCategoryReadOnlyViewSet, IncidentCategoryWriteViewSet

router = DefaultRouter()
router.register(r'', IncidentCategoryReadOnlyViewSet, basename='incident-category-read')
router.register(r'admin', IncidentCategoryWriteViewSet, basename='incident-category-manage')
# router.register(r'incidents', IncidentViewSet, basename='incident')

urlpatterns = [
    path('', include(router.urls)),
]
