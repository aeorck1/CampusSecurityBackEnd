# in your app's utils.py or a dedicated exceptions/handlers.py file

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError, NotAuthenticated, PermissionDenied, APIException
)
from django.http import Http404 # Django's 404
# Import or define your custom exceptions here, e.g.:
# from .exceptions import (
#     ApiBadRequestException, ApiNotFoundException, TenantCreationException,
#     InvalidTenantException, InvalidIssuerException, IssuerNotFoundException
# )

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework.
    Maps exceptions to custom response formats and status codes.
    """

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # This handles DRF's built-in exceptions (like ValidationError, NotAuthenticated, etc.)
    # and Django's Http404 and PermissionDenied.
    response = exception_handler(exc, context)

    custom_response_data = {
        'isError': True,
        'isSuccess': False,
        'timestamp': None, # You might add a timestamp here
        'description': 'An error occurred',
        'errors': {}
    }

    # If DRF's default handler provided a response, we can modify it
    if response is not None:
        custom_response_data['description'] = response.data.get('detail', 'Error')

        # Handle specific DRF exceptions
        if isinstance(exc, ValidationError):
            custom_response_data['description'] = 'Invalid Request'
            # DRF ValidationError detail can be a dict, list, or string
            # We'll format it to match the Java example's structure
            errors = {}
            if isinstance(response.data, dict):
                for field, messages in response.data.items():
                    # Ensure messages is a list/set
                    if not isinstance(messages, (list, set)):
                        messages = [messages]
                    errors[field] = set(messages) # Use a set to match Java example
            elif isinstance(response.data, list):
                 # Handle non-field errors if ValidationError detail is a list
                 errors['non_field_errors'] = set(response.data)
            else:
                 # Handle simple string detail
                 errors['detail'] = {response.data}

            custom_response_data['errors'] = errors

        elif isinstance(exc, (NotAuthenticated, PermissionDenied)):
             # These are often handled by DRF's default, but you can customize
             custom_response_data['description'] = 'Authentication or Permission Error'
             # The default handler usually puts detail in the response body
             if 'detail' in response.data:
                 custom_response_data['errors']['detail'] = {response.data['detail']}


        elif isinstance(exc, Http404):
             custom_response_data['description'] = 'Resource Not Found'
             if 'detail' in response.data:
                  custom_response_data['errors']['detail'] = {response.data['detail']}


        # You can add specific handling for other DRF exceptions here if needed
        # elif isinstance(exc, OtherDRFException):
        #     custom_response_data['description'] = '...'
        #     custom_response_data['errors'] = {...}


        # Update the response data with our custom structure
        response.data = custom_response_data

        return response

    # If DRF's default handler didn't produce a response, it might be
    # a non-DRF exception or a custom exception we need to handle.
    # This acts as the equivalent of your handleSecurityException and other
    # specific handlers in the Java @RestControllerAdvice.

    # You would add checks for your specific custom exceptions here:
    # if isinstance(exc, ApiBadRequestException):
    #     custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Bad Request'
    #     status_code = status.HTTP_400_BAD_REQUEST
    # elif isinstance(exc, ApiNotFoundException):
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Resource Not Found'
    #      status_code = status.HTTP_404_NOT_FOUND
    # elif isinstance(exc, TenantCreationException):
    #     custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Tenant Could not be created'
    #     status_code = status.HTTP_417_EXPECTATION_FAILED # Using 417 for EXPECTATION_FAILED
    # elif isinstance(exc, InvalidTenantException):
    #     custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Unknown Tenant'
    #     status_code = status.HTTP_417_EXPECTATION_FAILED
    # elif isinstance(exc, InvalidIssuerException):
    #     custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Invalid Issuer'
    #     status_code = status.HTTP_400_BAD_REQUEST
    # elif isinstance(exc, IssuerNotFoundException):
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'Unknown Issuer'
    #      status_code = status.HTTP_400_BAD_REQUEST
    # elif isinstance(exc, BadCredentialsException): # You might have a Python equivalent exception
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'The username or password is incorrect'
    #      status_code = status.HTTP_400_BAD_REQUEST
    # elif isinstance(exc, AccountStatusException): # You might have a Python equivalent exception
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'The account is locked'
    #      status_code = status.HTTP_403_FORBIDDEN
    # elif isinstance(exc, AccessDeniedException): # You might have a Python equivalent exception
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'You are not authorized to access this resource'
    #      status_code = status.HTTP_403_FORBIDDEN
    # elif isinstance(exc, SignatureException): # You might have a Python equivalent exception for JWT signature errors
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'The JWT signature is invalid'
    #      status_code = status.HTTP_403_FORBIDDEN
    # elif isinstance(exc, (ExpiredJwtException, InvalidBearerTokenException, JwtValidationException)): # Python equivalents
    #      custom_response_data['description'] = exc.detail if hasattr(exc, 'detail') else 'The JWT token has expired'
    #      status_code = status.HTTP_403_FORBIDDEN


    # Generic exception handling (catch-all)
    else:
        logger.exception("An unhandled exception occurred") # Log the exception
        custom_response_data['description'] = 'An unexpected server error occurred.'
        custom_response_data['errors']['detail'] = {'We will fix it shortly.'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # Default to 500 for unhandled errors

    # For exceptions not handled by the default handler but caught here
    if 'status_code' not in locals():
         status_code = getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
         if isinstance(exc, APIException) and hasattr(exc, 'detail'):
             custom_response_data['errors']['detail'] = {exc.detail}


    # Return the custom response
    return Response(custom_response_data, status=status_code)

# In your settings.py:

# Add this to your settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'your_app_name.utils.custom_exception_handler' # Replace 'your_app_name.utils' with the actual path
}

# Define custom exceptions (optional, but good practice)
# in your app's exceptions.py

# from rest_framework.exceptions import APIException

# class ApiBadRequestException(APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = 'Bad Request'
#     default_code = 'bad_request'

# class ApiNotFoundException(APIException):
#     status_code = status.HTTP_404_NOT_FOUND
#     default_detail = 'Resource Not Found'
#     default_code = 'not_found'

# # Define other custom exceptions as needed, inheriting from APIException
# class TenantCreationException(APIException):
#     status_code = status.HTTP_417_EXPECTATION_FAILED
#     default_detail = 'Tenant Could not be created'
#     default_code = 'tenant_creation_failed'

# ... and so on for other custom exceptions