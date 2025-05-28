from rest_framework import serializers

from api.system_administration.role.serializers import RoleSerializer
from appdata.models import User


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

