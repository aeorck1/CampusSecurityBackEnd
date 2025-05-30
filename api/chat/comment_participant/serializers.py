from rest_framework import serializers


class CommentCountSerializer(serializers.Serializer):
    object_type = serializers.CharField()
    object_id = serializers.CharField()
    total_count = serializers.IntegerField()
    last_count = serializers.IntegerField()
