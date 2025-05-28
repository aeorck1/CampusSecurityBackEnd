from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone

from core.api.exceptions.exc import TokenValidationError


def jwt_encode(payload, expires_in=3600):
    payload['iat'] = timezone.now()
    payload['exp'] = timezone.now() + timedelta(seconds=expires_in)

    return jwt.encode(payload, settings.JWT_SECRET_KEY ,algorithm=settings.JWT_ALGORITHM)


def jwt_decode(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenValidationError("Token is expired")
    except jwt.InvalidTokenError:
        raise TokenValidationError("Invalid token")
