from rest_framework import serializers

from api.chat.comment.services import CommentService
from api.serializers import UserAuditOnValidateSerializer
from api.system_administration.user.serializers import MinimalUserSerializer
from appdata.models import Comment


class CommentListSerializer(serializers.ModelSerializer):

    comment_by = MinimalUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentAddSerializer(UserAuditOnValidateSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'position', 'comment_by', 'parent_comment_metadata')

    def create(self, validated_data):
        validated_data['comment_by'] = self.context['request'].user
        return CommentService.add_comment(validated_data)


class CommentUpdateSerializer(UserAuditOnValidateSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'position', 'comment_by', 'parent_comment_metadata', 'parent_comment', 'object_id', 'object_type')

    def update(self, instance, validated_data):
        return CommentService.update_comment(instance, validated_data)
