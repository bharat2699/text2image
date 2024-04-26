from rest_framework import serializers


class TtiRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        required=True,
        max_length=2000,
        min_length=3,
        allow_blank=False,
        allow_null=False,
        error_messages={
            "required": "Text is required",
            "blank": "Text cannot be blank",
            "min_length": "Text must be at least 3 characters long",
            "max_length": "Text cannot be more than 2000 characters long",
        },
    )


class TtiResponseSerializer(serializers.Serializer):
    requestId = serializers.UUIDField(
        required=True,
        allow_null=False,
        error_messages={
            "required": "Request ID is required",
            "null": "Request ID cannot be null",
            "invalid": "Request ID is invalid",
        },
    )
