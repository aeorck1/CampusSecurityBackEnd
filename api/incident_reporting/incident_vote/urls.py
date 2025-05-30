from django.urls import path

from api.incident_reporting.incident_vote.views import IncidentVoteView

urlpatterns = [
    path('incident-votes/', IncidentVoteView.as_view(), name='incident-vote'),
]
