import threading

from django.contrib.auth.models import AnonymousUser


_request = threading.local()
_context_user = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the request in the thread-local variable
        _request.value = request
        response = self.get_response(request)
        return response


class ContextUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _context_user.value = request.user
        response = self.get_response(request)
        return response


def get_current_request():
    """Retrieve the current request from thread-local storage."""
    return getattr(_request, 'value', None)


def get_context_user():
    """
    Returns the current user from the thread local storage.
    If there's no user in thread local storage, tries to get it from the request.
    Returns AnonymousUser if no user is found.
    """

    user = getattr(_context_user, 'value', None)
    if user is not None:
        return user

    request = get_current_request()
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        return request.user

    return AnonymousUser()
