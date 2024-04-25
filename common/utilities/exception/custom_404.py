from rest_framework.response import Response
from rest_framework.decorators import api_view

from common.helpers.constants import StatusCodes


@api_view(("GET", "POST", "PUT", "PATCH", "DELETE"))
def custom404(*_, **kwargs):
    return Response(
        {
            "success": False,
            "code": StatusCodes().NOT_FOUND,
            "message": "Page not found.",
        },
        status=StatusCodes().NOT_FOUND,
    )
