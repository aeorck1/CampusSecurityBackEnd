from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.system_administration.user.serializers import MinimalUserSerializer
from api.system_administration.user.services import UserService


@extend_schema_view(
    get=extend_schema(summary='Retrieve the lists of users',
                      description='Retrieve the lists of users.',
                      tags=['Users'])
)
class UserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MinimalUserSerializer
    queryset = UserService.get_users()

