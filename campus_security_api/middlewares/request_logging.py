import logging
import time
from typing import Callable

from django.http import HttpRequest, HttpResponse

# Get a logger instance (configure this in your Django settings)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware that logs the start and end time of each request,
    along with the total duration.
    """
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        """
        Initialize the middleware. Needs the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and response.
        """
        start_time = time.time()
        # Store start time on the request object itself for later access
        # This is generally safe within a single request lifecycle
        request.start_time = start_time

        # --- Equivalent to preHandle ---
        # Log before processing the view
        logger.info(f"API call started: {request.method} {request.get_full_path()}")

        # Process the request: pass control to the next middleware or the view
        response = self.get_response(request)

        # --- Equivalent to postHandle ---
        # This code executes after the view has been processed successfully
        # Note: If the view raises an exception, this part might be skipped
        # unless wrapped in a try...finally (see alternative below).

        try:
            # Retrieve start time from the request
            start_time_req = getattr(request, 'start_time', None)
            if start_time_req:
                end_time = time.time()
                duration_ms = (end_time - start_time_req) * 1000 # Convert to milliseconds
                logger.info(
                    f"API call ended:   {request.method} {request.get_full_path()} "
                    f"Status: {response.status_code} Duration: {duration_ms:.2f} ms"
                )
            else:
                # Should ideally not happen if preHandle part executed
                 logger.warning(f"API call ended but start time not found: {request.method} {request.get_full_path()}")

        except Exception as e:
            # Log if there's an error during the post-processing logging itself
            logger.exception(f"Error logging API call end: {e}")


        # --- Equivalent to afterCompletion ---
        # The code after self.get_response() runs after the view.
        # For cleanup or logging that *must* run even if the view fails,
        # you could use a try...finally block around `response = self.get_response(request)`.
        # The example above logs duration only on successful view execution + response generation,
        # similar to how postHandle works (which isn't called if the handler throws an exception).

        return response

    # Optional: If you need specific exception handling (like Spring's afterCompletion(ex))
    # you can implement process_exception, though duration logging often
    # happens within __call__ using try/finally if needed for exceptions too.
    # def process_exception(self, request: HttpRequest, exception: Exception):
    #     logger.error(f"API call exception: {request.method} {request.get_full_path()} Exception: {exception}")
    #     # Return None to let default exception handling continue
    #     return None