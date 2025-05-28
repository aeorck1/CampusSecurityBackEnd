
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.api.exceptions.exc import TokenExpiredException, InvalidTokenException


class BearerToken:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


class JwtService:

    user_model = get_user_model()

    @classmethod
    def generate_tokens(cls, user: user_model):
        now = timezone.now()

        access_payload = {
            'user_id': user.id,
            'email': user.email,
            'type': 'access',
            'exp': now + settings.JWT_ACCESS_TOKEN_LIFETIME,
            'iat': now
        }

        refresh_payload = {
            'user_id': user.id,
            'type': 'refresh',
            'exp': now + settings.JWT_REFRESH_TOKEN_LIFETIME,
            'iat': now
        }

        access_token = jwt.encode(access_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return BearerToken(access_token, refresh_token)

    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenException("Invalid token")
