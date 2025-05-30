from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.incident_reporting.incident_vote.serializers import IncidentVoteSerializer
from appdata.models import Incident
from appdata.models import IncidentVote


class IncidentVoteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Upvote or Downvote an Incident",
        description="Allows a logged-in user to upvote or downvote an incident. Pass 'incident_id' and 'up_voted'.",
        request=IncidentVoteSerializer,
        tags=['Incident']
    )
    def post(self, request):
        serializer = IncidentVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        incident_id = serializer.validated_data['incident_id']
        up_voted = serializer.validated_data['up_voted']
        user = request.user

        incident = get_object_or_404(Incident, id=incident_id)

        # Check if the user has already voted
        vote, created = IncidentVote.objects.get_or_create(
            incident=incident,
            created_by_user=user,
            defaults={'up_voted': up_voted}
        )

        if not created:
            # Update the existing vote
            vote.up_voted = up_voted
            vote.save()
            action = "updated"
        else:
            action = "created"

        return Response({
            "message": f"Vote {action} successfully",
            "incident_id": str(incident_id),
            "up_voted": up_voted
        }, status=status.HTTP_200_OK)
