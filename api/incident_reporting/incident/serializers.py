from django.utils import timezone
from rest_framework import serializers

from api.chat.comment.serializers import CommentListSerializer
from api.incident_reporting.incident_category.serializers import IncidentTagSerializer
from api.system_administration.user.serializers import MinimalUserSerializer
from appdata.model_util import jsonify_user
from appdata.models import Incident
from appdata.models import IncidentTag
from appdata.models.incident import IncidentStatus


class IncidentSerializer(serializers.ModelSerializer):
    tags = IncidentTagSerializer(many=True, read_only=True)
    reported_by = MinimalUserSerializer(read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    up_votes = serializers.IntegerField(read_only=True)
    down_votes = serializers.IntegerField(read_only=True)


    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['reported_by', 'up_votes', 'down_votes', 'status', 'id', 'date_created', 'date_last_modified', 'reporter_satisfaction', 'date_resolved']  # status updated via separate view


class IncidentCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentTag.objects.all(), required=True)

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['status', 'reported_by', 'id', 'date_created', 'date_last_modified', 'created_by_user', 'last_modified_by_user', 'reporter_satisfaction', 'date_resolved']  # reported_by filled later for auth users


class IncidentStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=True)
    class Meta:
        model = Incident
        fields = ['status']


    def validate(self, attrs):
        attrs['last_modified_by_user'] = jsonify_user(self.context['request'].user)
        if attrs['status'] == IncidentStatus.RESOLVED.name:
            attrs['date_resolved'] = timezone.now()
        return attrs



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
