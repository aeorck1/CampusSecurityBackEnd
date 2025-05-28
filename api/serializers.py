"""Global serializer definitions for the entire API module"""
from rest_framework import serializers

from appdata.model_util import jsonify_user


class ContextUserAsJsonDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return jsonify_user(serializer_field.context['request'].user)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ContextUser:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class UserAuditSerializer(serializers.ModelSerializer):
    created_by_user = serializers.JSONField(default=ContextUserAsJsonDefault(), read_only=True)
    last_modified_by_user = serializers.JSONField(read_only=True)

    def create(self, validated_data):
        validated_data['created_by_user'] = jsonify_user(self.context['request'].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['last_modified_by_user'] = jsonify_user(self.context['request'].user)
        return super().update(instance, validated_data)


class UserAuditOnValidateSerializer(serializers.ModelSerializer):
    created_by_user = serializers.JSONField(default=ContextUserAsJsonDefault(), read_only=True)
    last_modified_by_user = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        if self.instance is not None:
            attrs['last_modified_by_user'] = jsonify_user(self.context['request'].user)
        else:
            attrs['created_by_user'] = jsonify_user(self.context['request'].user)

        return attrs
