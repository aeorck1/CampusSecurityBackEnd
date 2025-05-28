from rest_framework import status
from rest_framework.response import Response

from core.api.reponses.serializers import ApiResponseSerializer, ApiResponse


class AppResponseMixin:
    """
    Mixin to wrap successful responses in an AppResponse structure,
    unless the view method is marked with @ignore_response_binding
    or the response indicates an error.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        # Check if the view method is marked to ignore binding
        # 'self.action' holds the name of the method being executed (e.g., 'list', 'create', 'retrieve')
        # method = getattr(self, self._current_action, None)
        # if method and getattr(method, 'ignore_response_binding', False):
        #     return super().finalize_response(request, response, *args, **kwargs)

        # Check if the response is an error response (typically based on status code)
        # DRF's default exception handler sets appropriate status codes for errors (>= 400)
        if status.is_client_error(response.status_code) or status.is_server_error(response.status_code):
            # Error responses are usually already formatted by the exception handler,
            # or we don't want to wrap them in the success envelope.
            return super().finalize_response(request, response, *args, **kwargs)

        # Also, avoid wrapping responses that are already AppResponse-like
        # You might add more robust checks here if your error responses also
        # have a similar structure but with isError=True
        # if isinstance(response.data, dict) and ('isSuccess' in response.data or 'isError' in response.data):
        #      return super().finalize_response(request, response, *args, **kwargs)


        # Wrap the successful response data
        # If the response data is None (e.g., 204 No Content), handle that
        data = ApiResponse(data=response.data, status_code=response.status_code)
        wrapped_data = data.__dict__

        # Create a new Response object with the wrapped data
        # Keep the original status code and headers
        response = Response(data=wrapped_data, status=response.status_code, headers=response._headers)

        return super().finalize_response(request, response, *args, **kwargs)

    # Helper to get the currently executing action method name
    # @property
    # def _current_action(self):
    #     # This is a bit of a workaround to get the current method name in finalize_response
    #     # which is not directly available as self.action like in the view methods themselves.
    #     # It assumes the view follows standard DRF routing where the action name is set.
    #     # More robust ways might involve storing the action name during dispatch.
    #     return getattr(self, 'action', request.method.lower()) # Fallback to method if action is not set