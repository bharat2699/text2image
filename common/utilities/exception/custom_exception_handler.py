from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    exc_type = type(exc).__name__
    exc_message = str(exc)

    logger.error(f"{exc_type}: {exc_message}", exc_info=True)

    # Check if the exception is a ValidationError
    if isinstance(exc, ValidationError):
        # Customize the response for ValidationError
        return Response(
            {
                "success": False,
                "code": status.HTTP_400_BAD_REQUEST,
                "errors": exc.detail,
                "message": f"{exc_type}: {exc_message}",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Now add the HTTP status code to the response.
    if response is None:
        return Response(
            {
                "success": False,
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": f"{exc_type}: {exc_message}",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data["error"] = exc_message
    if type(response.data["detail"].code) == int:
        response.data["code"] = response.data["detail"].code
    else:
        response.data["code"] = response.status_code
    # Add custom error message to the response
    return Response(
        {
            "success": False,
            "code": response.data["code"],
            "errors": exc_message,
            "message": f"{exc_type}: {exc_message}",
        },
        status=response.data["code"],
    )
