from django.utils import timezone
from rest_framework import serializers
from appdata.models import Incident
from appdata.models import IncidentCategory
from appdata.models.incident import IncidentStatus


class IncidentSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentCategory.objects.all(), required=True)

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['reported_by', 'status', 'id', 'date_created', 'date_last_modified', 'reporter_satisfaction', 'date_resolved']  # status updated via separate view


class IncidentCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentCategory.objects.all(), required=True)

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['status', 'reported_by', 'id', 'date_created', 'date_last_modified', 'created_by_user', 'last_modified_by_user', 'reporter_satisfaction', 'date_resolved']  # reported_by filled later for auth users


class IncidentStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=True)
    class Meta:
        model = Incident
        fields = ['status']


    def update(self, instance, validated_data):
        if validated_data['status'] == IncidentStatus.RESOLVED.name:
            validated_data['date_resolved'] = timezone.now()


class IncidentStatisticsSerializer(serializers.Serializer):
    total_incidents = serializers.IntegerField()
    active_incidents = serializers.IntegerField()
    resolved_incidents = serializers.IntegerField()
    investigating_incidents = serializers.IntegerField()
    average_response_time = serializers.CharField()  # includes unit
    average_satisfaction = serializers.FloatField(allow_null=True)


class IncidentSatisfactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['reporter_satisfaction']
        extra_kwargs = {
            'reporter_satisfaction': {'required': True, 'min_value': 0, 'max_value': 1}
        }
