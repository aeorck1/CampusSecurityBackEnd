def jsonify_user(instance) -> dict:
    if instance is None:
        return {}
    return {
        'id': instance.id,
        'email': instance.email,
        'username': instance.username,
        'role_id': instance.role.id,
        'first_name': instance.first_name
    }
