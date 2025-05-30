from rest_framework import serializers

from appdata.models import IncidentTag


class IncidentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentTag
        fields = '__all__'
