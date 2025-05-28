

def update_object_attributes(instance: object, validated_data: dict[str, object]) -> object:

    # Update fields on the instance
    for key, value in validated_data.items():
        if hasattr(instance, key):
            setattr(instance, key, value)

    return instance
