from common.helpers.constants import StatusCodes
from common.utilities.service.base_service import BaseService
from text_to_image.tasks.sd_tasks import SdTasks
from ..models.text_to_image import TextToImage
from rest_framework import exceptions


class TtiServices(BaseService):
    def __init__(self):
        self.task = SdTasks()

    def post_service(self, request, data):
        prompt = data.get("text")
        create_tti_model_instance = TextToImage.objects.create(prompt=prompt)
        self.task.delay(
            {"prompt": prompt, "request_id": str(create_tti_model_instance.uuid)}
        )
        response_data = {"requestId": str(create_tti_model_instance.uuid)}
        return self.ok(response_data, StatusCodes().CREATED)

    def get_service(self, request, data):
        request_id = data.get("requestId")
        tti_model_instance = TextToImage.objects.filter(uuid=request_id).first()

        if not tti_model_instance:
            raise exceptions.APIException(
                "Request ID not found", StatusCodes().NOT_FOUND
            )
        if tti_model_instance.status == "pending":
            raise exceptions.APIException(
                "Request is still in progress", StatusCodes().NO_CONTENT
            )

        if tti_model_instance.status == "failed":
            raise exceptions.APIException(
                "Request failed, try again", StatusCodes().BAD_REQUEST
            )

        response_data = {
            "requestId": str(tti_model_instance.uuid),
            "imageUrl": tti_model_instance.image_url,
            "status": tti_model_instance.status,
        }
        return self.ok(response_data, StatusCodes().SUCCESS)
