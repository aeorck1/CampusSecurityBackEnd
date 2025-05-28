from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.services.jwt_service import JwtService


class JWTAuthentication(BaseAuthentication):

    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header: str = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith(f'{self.keyword} '):
            return None

        token = auth_header.split(' ', 1)[1]

        try:
            payload = JwtService.decode_token(token)
            if payload['type'] != 'access':
                raise AuthenticationFailed('Invalid token type')

            user = get_user_model().objects.get(id=payload['user_id'])

            return user, token
        except Exception as e:
            raise AuthenticationFailed(str(e))


class JwtTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'api.system_administration.auth.authentication.JWTAuthentication'
    name = 'JwtAuthToken'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix=self.target.keyword,
        )
