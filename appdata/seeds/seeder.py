import os

from appdata.managers import DefaultRoles
from appdata.model_util import jsonify_user
from appdata.models.user import User


class Seeder:
    system_user_id = 'system'

    @classmethod
    def _get_created_by_user(cls, apps):
        # User = apps.get_model("appdata", "User")

        return jsonify_user(User.objects.get(pk=cls.system_user_id))

    @classmethod
    def insert_default001_roles(cls, apps, schema_editor):
        Role = apps.get_model("appdata", "Role")

        # Default Values for Role
        roles = [
            {
                "id": DefaultRoles.SYSTEM_ADMIN.name,
                "name": DefaultRoles.SYSTEM_ADMIN.value,
                "description": "System Administrator",
            },
            {
                "id": DefaultRoles.ADMIN.name,
                "name": DefaultRoles.ADMIN.value,
                "description": "Administrator",
            },
            {
                "id": DefaultRoles.STUDENT.name,
                "name": DefaultRoles.STUDENT.value,
                "description": "Student"
            }
        ]

        for data in roles:
            Role.objects.create(**data)

    @classmethod
    def insert_default002_system_user(cls, apps, schema_editor):
        # User = apps.get_model("appdata", "User")
        
        user = {
            'id': cls.system_user_id,
            'email': 'system@campussecurity.com',
            'password': os.getenv('SYSTEM_USER_PASSW'),
            'username': 'system',
            'first_name': 'Security',
            'last_name': 'Admin',
        }

        User.objects.create_superuser(**user)

    @classmethod
    def insert_default003_incident_category(cls, apps, schema_editor):
        IncidentCategory = apps.get_model("appdata", "IncidentCategory")

        created_by = cls._get_created_by_user(apps)

        categories = [
            {
                "id": "property_damage",
                "name": "Property Damage",
                'created_by_user': created_by,
            },
            {
                "id": "safety_hazard",
                "name": "Safety Hazard",
                'created_by_user': created_by,
            },
            {
                "id": "security_concern",
                "name": "Security Concern",
                'created_by_user': created_by,
            },
            {
                "id": "theft",
                "name": "Theft",
                'created_by_user': created_by,
            },
            {
                "id": "vandalism",
                "name": "Vandalism",
                'created_by_user': created_by,
            },
            {
                "id": "suspicious_activity",
                "name": "Suspicious Activity",
                'created_by_user': created_by,
            },
            {
                "id": "facility_issues",
                "name": "Facility Issue",
                'created_by_user': created_by,
            },
            {
                "id": "accessibility_issues",
                "name": "Accessibility Issue",
                'created_by_user': created_by,
            },
            {
                "id": "other",
                "name": "Other",
                'created_by_user': created_by,
            },
        ]

        for data in categories:
            IncidentCategory.objects.create(**data)
