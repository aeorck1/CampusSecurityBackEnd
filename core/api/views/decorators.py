from functools import wraps


def ignore_response_binding(func):
    """
    Decorator to mark view methods whose responses should not be wrapped
    by the AppResponseMixin.
    """
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        return func(*args, **kwargs)
    wrapped_func.ignore_response_binding = True
    return wrapped_func