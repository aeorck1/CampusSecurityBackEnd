from typing import Any


def jsonify_user(instance) -> dict[str, Any] | None:
    if instance is None or instance.is_anonymous:
        return None
    return {
        'id': instance.id,
        'email': instance.email,
        'username': instance.username,
        'role_id': instance.role.id,
        'first_name': instance.first_name
    }
