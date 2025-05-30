from django.urls import include, path

urlpatterns = [
    path("incident-categories/", include("api.incident_reporting.incident_category.urls")),
    path("", include("api.incident_reporting.incident.urls")),
    path("", include("api.incident_reporting.incident_vote.urls")),
]