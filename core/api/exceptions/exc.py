from django.utils.translation import gettext_lazy as _
import logging

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

logger = logging.getLogger(__name__)


class BaseApiException(APIException):
    """
    Base custom exception for the API.
    Adds user-friendly and developer-friendly message fields.
    """
    user_message = None
    developer_message = None

    def __init__(self, detail=None, code=None, user_message=None, developer_message=None):
        super().__init__(detail, code)

        self.user_message = user_message if user_message is not None else self.user_message
        self.developer_message = developer_message if developer_message is not None else self.developer_message

        # Optional: Log the developer message when the exception is created
        if self.developer_message:
            logger.error(f"Developer Error: {self.developer_message}", exc_info=True)
            logger.error(f"Developer Error in {self.__class__.__name__}: {self.developer_message}")


# --- Specific Exception Classes Inheriting from BaseApiException ---

class BadRequestException(BaseApiException):
    """
    Custom exception for 400 Bad Request errors.
    Use for general client input errors not covered by validation errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request.')
    default_code = 'bad_request'
    user_message = _('The request was invalid.')


class ResourceNotFoundException(BaseApiException):
    """
    Custom exception for 404 Not Found errors.
    Use when a specific resource is not found.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Not found.')
    default_code = 'not_found'
    user_message = _('The requested item was not found.')


# Note: While you can define custom exceptions for 401 and 403,
# DRF's built-in NotAuthenticated (401) and PermissionDenied (403)
# are often sufficient and well-integrated with DRF's auth/permissions.
# If you need custom messages or developer info, inheriting is useful.

class AuthenticationFailedException(BaseApiException):
    """
    Custom exception for 401 Authentication Failed errors.
    Use when authentication credentials are not provided or are invalid.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated' # Matching DRF's default code
    user_message = _('Please log in to access this resource.')
#
#
# class PermissionDeniedException(BaseApiException):
#     """
#     Custom exception for 403 Permission Denied errors.
#     Use when the user is authenticated but does not have permissions.
#     """
#     status_code = status.HTTP_403_FORBIDDEN
#     default_detail = _('You do not have permission to perform this action.')
#     default_code = 'permission_denied' # Matching DRF's default code
#     user_message = _('You are not allowed to perform this action.')


class InternalServerError(BaseApiException):
    """
    Custom exception for 500 Internal Server Errors for *handled* server issues.
    Note: Most unhandled Python exceptions will still fall into the generic
    500 handling in your custom_exception_handler's else block.
    This class is for situations where you explicitly want to raise a 500
    for a known server-side issue that prevents fulfilling the request.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Internal server error.')
    default_code = 'internal_error'
    user_message = _('An unexpected error occurred on the server.')
    # developer_message is particularly useful for 500 errors


class InvalidInputException(BadRequestException):
    default_detail = _('Invalid input provided.')
    default_code = 'invalid_input'
    user_message = _('Please check the data you entered.')


class TokenExpiredException(AuthenticationFailedException):
    default_detail = _('Expired token has expired.')
    default_code = 'expired_token'
    user_message = _('The authentication token has expired.')


class InvalidTokenException(AuthenticationFailedException):
    default_detail = _('Invalid token has expired.')
    default_code = 'invalid_token'
    user_message = _('The authentication token is invalid.')


class TokenValidationError(ValidationError):
    default_detail = _('Token is not valid')
    default_code = 'token_validation_error'
