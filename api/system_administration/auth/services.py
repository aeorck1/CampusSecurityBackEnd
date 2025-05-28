from types import SimpleNamespace

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed

from api.system_administration.user.services import UserService
from core.api.exceptions.exc import BadRequestException, InvalidTokenException
from core.services.jwt_service import JwtService, BearerToken


class AuthenticationService:

    @classmethod
    def authenticate(cls, request, username, password) -> SimpleNamespace:

        user = authenticate(request=request, username=username, password=password)

        if not user:
            msg = _('Unable to authenticate with the provided credentials')
            raise AuthenticationFailed(msg)

        bearer_token = JwtService.generate_tokens(user)



        return SimpleNamespace(access_token=bearer_token.access_token,
                               refresh_token=bearer_token.refresh_token,
                               username=username,
                               user=user)


    @classmethod
    def refresh_token(cls, token: str) -> BearerToken:

        payload = JwtService.decode_token(token)
        if payload['type'] != 'refresh':
            raise BadRequestException("Invalid token type")

        user = UserService.get_user(payload['user_id'])

        return JwtService.generate_tokens(user)

    @classmethod
    def verify_token(cls, token: str):

        try:
            payload = JwtService.decode_token(token)

            return SimpleNamespace(valid=True, payload=payload)
        except:
            raise InvalidTokenException("Token is invalid.")
