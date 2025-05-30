from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.system_administration.user.serializers import MinimalUserSerializer, StudentRegistrationSerializer, \
    UserProfileUpdateSerializer
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


@extend_schema(
    summary="Student Registration",
    description="Register a new student user account.",
    tags=["Users"]
)
class StudentRegistrationView(CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = []  # Allow anyone to register


@extend_schema_view(
    put=extend_schema(summary="Update User Profile",
                      description="Allows the authenticated user to update their profile fields: names, department, bio, and profile picture.",
                      request=UserProfileUpdateSerializer,
                      tags=['User'])
)
class UserProfileUpdateView(UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        # Return the current logged-in user
        return self.request.user
