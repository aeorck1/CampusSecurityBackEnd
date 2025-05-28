from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.system_administration.auth.services import AuthenticationService
from api.system_administration.user.serializers import UserSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,
                                     help_text=_('Account Email or username'))
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=True
    )

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        return AuthenticationService.authenticate(
            request=self.context.get('request'),
            username=validated_data['username'],
            password=validated_data['password']
        )


class RefreshTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        return AuthenticationService.refresh_token(
            token=validated_data['refresh_token']
        )


class TokenValidationSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    valid = serializers.BooleanField(read_only=True)
    payload = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return AuthenticationService.verify_token(token=validated_data['token'])