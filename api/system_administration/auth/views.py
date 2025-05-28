from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.system_administration.auth.serializers import LoginSerializer, RefreshTokenSerializer, \
    TokenValidationSerializer, PasswordResetRequestSerializer, PasswordResetCompleteSerializer
from api.system_administration.user.services import UserService
from core.api.exceptions.exc import ResourceNotFoundException, TokenValidationError
from core.services.email_service import EmailMulti
from core.utils.jwt_utils import jwt_encode, jwt_decode


@extend_schema(
    summary='Obtain access and refresh tokens',
    tags=['Authentication']
)
class ObtainTokenPairView(CreateAPIView):
    serializer_class = LoginSerializer


@extend_schema(
    summary='Refresh access token',
    tags=['Authentication']
)
class RefreshTokenView(CreateAPIView):
    serializer_class = RefreshTokenSerializer


@extend_schema(
    summary='Verify access token',
    tags=['Authentication']
)
class VerifyTokenView(CreateAPIView):
    serializer_class = TokenValidationSerializer


class PasswordResetRequestView(APIView):
    @extend_schema(
        summary="Initiate Password Reset",
        description="Request a password reset link via email.",
        tags=["Authentication"],
        request=PasswordResetRequestSerializer,
        responses={200: serializers.Serializer()}  # Empty serializer for simple response
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = UserService.get_user_by_email_or_username(email)
        except ResourceNotFoundException:
            return Response({"detail": "If this email is registered, you will receive a password reset link."},
                            status=200)

        # Generate JWT token
        payload = {
            "user_id": user.id,
            "email": user.email
        }

        token = jwt_encode(payload)

        # Build reset link
        reset_link = f"{settings.PASSWORD_RESET_URL}?token={token}"

        # Send email
        EmailMulti(
            subject="Password Reset Request",
            text_body=f"Click the link to reset your password: {reset_link}",
            recipient_list=[user.email]
        ).send_bg()

        return Response({"detail": "If this email is registered, you will receive a password reset link."}, status=200)


class PasswordResetCompleteView(APIView):
    @extend_schema(
        summary="Complete Password Reset",
        description="Set a new password using the token from the reset link.",
        tags=["Authentication"],
        request=PasswordResetCompleteSerializer,
        responses={200: serializers.Serializer()}  # Empty serializer for simple response
    )
    def post(self, request):
        serializer = PasswordResetCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            payload = jwt_decode(token)

            user_id = payload.get("user_id")
            user = UserService.get_user(user_id)
        except (TokenValidationError, ResourceNotFoundException):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
