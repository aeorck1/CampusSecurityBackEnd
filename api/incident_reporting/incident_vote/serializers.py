from rest_framework import serializers


class IncidentVoteSerializer(serializers.Serializer):
    incident_id = serializers.CharField()
    up_voted = serializers.BooleanField()
