from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.system_administration.role.serializers import RoleSerializer
from appdata.managers import DefaultRoles
from appdata.models import User, Role


class UserSerializer(serializers.ModelSerializer):

    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {'input_type': 'password'},
                'trim_whitespace': False
            },
        }

class MinimalUserSerializer(serializers.ModelSerializer):

    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'role', 'first_name', 'last_name', 'middle_name', 'email')


class StudentRegistrationSerializer(serializers.ModelSerializer):

    role = RoleSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'role', 'date_joined', 'last_login')
        read_only_fields = ('date_joined', 'last_login', 'id', 'role')

    def create(self, validated_data):
        # Fetch the student role (ensure the 'student' role exists in Role table)
        try:
            student_role = Role.objects.get(id=DefaultRoles.STUDENT.name)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Student role is not configured in the system.")

        validated_data['role'] = student_role
        return User.objects.create_user(**validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'department', 'bio', 'profile_picture']
