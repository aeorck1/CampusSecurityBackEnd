from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from api.system_administration.auth.serializers import LoginSerializer, RefreshTokenSerializer, \
    TokenValidationSerializer


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
