import typing as _
from rest_framework.views import APIView
from rest_framework.response import Response
from common.helpers.constants import StatusCodes

T = _.TypeVar("T")


class BaseAPIView(APIView):
    def success(
        self, data: T, code=StatusCodes().SUCCESS, msg: _.Optional[str] = None
    ) -> Response:
        return Response(
            {
                "success": True,
                "code": code,
                "data": data,
                "message": msg,
            },
            status=code,
        )

    def error(self, errors: T, status_code: int) -> Response:
        return Response(
            {"success": False, "code": status_code, "errors": errors},
            status=status_code,
        )

    def validation_failed(self, **kwargs) -> Response:
        return self.error(kwargs, StatusCodes().UNPROCESSABLE_ENTITY)

    def error_message(
        self, msg: str, code: int, data: _.Optional[dict] = None
    ) -> Response:
        return Response(
            {"success": False, "code": code, "message": msg, "data": data}, status=code
        )

    def error_message_without_data(self, msg: str, code: int) -> Response:
        return Response(
            {
                "success": False,
                "code": code,
                "message": msg,
            },
            status=code,
        )

    def no_content(self) -> Response:
        return Response(status=StatusCodes().NO_CONTENT)
