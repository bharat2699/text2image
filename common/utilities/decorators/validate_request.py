import typing as _
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from common.helpers.constants import StatusCodes


def validate_request(serializer: _.Type[serializers.Serializer]) -> _.Callable:

    def decorator(func: _.Callable):
        def wrapper(self, req: Request, *args, **kwargs):
            query_params = {}
            # Ignoring extra query params with the same key name
            for key in req.query_params:
                query_params[key] = req.query_params[key]

            # Creating serializer from query params and request body
            _all = {**req.data, **query_params, **kwargs}
            serialized = serializer(data=_all)

            # Validating data
            if not serialized.is_valid():
                # Building error messages
                errors = []
                for error in serialized.errors:
                    field = error
                    message = str(
                        serialized.errors[error][0]
                        if isinstance(serialized.errors[error], list)
                        else serialized.errors[error]
                    )
                    errors.append(
                        {
                            "field": field,
                            "message": message,
                        }
                    )

                return Response(
                    {
                        "code": StatusCodes().UNPROCESSABLE_ENTITY,
                        "message": "Validation Failed",
                        "errors": errors,
                    },
                    status=StatusCodes().UNPROCESSABLE_ENTITY,
                )

            # Calling view method
            return func(self, req, serialized.data, *args)

        return wrapper

    return decorator
