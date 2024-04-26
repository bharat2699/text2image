from celery.utils.log import get_task_logger
from common.utilities.aws.s3 import AwsS3Client
from text2image import celery_app, settings
import celery
import base64
import io
import requests

from text_to_image.models.text_to_image import TextToImage

logger = get_task_logger(__name__)
engine_id = settings.SD_ENGINE_ID
api_host = settings.SD_BASE_URL
api_key = settings.SD_API_KEY


class SdTasks(celery.Task):
    name = "process_sd_task"

    def __init__(self):
        self.s3 = AwsS3Client(settings.S3_BUCKET)

    def run(self, data):
        try:
            tti_model_instance = TextToImage.objects.get(uuid=data.get("request_id"))
            payload = {
                "text_prompts": [{"text": data.get("prompt")}],
                "cfg_scale": 10,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            }
            response = requests.post(
                f"{api_host}/v1/generation/{engine_id}/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json=payload,
            )

            tti_model_instance.sd_api_request = payload

            if response.status_code != 200:
                tti_model_instance.status = "failed"
                tti_model_instance.sd_api_response = response.json()
                tti_model_instance.save()
                return "process_sd_task_failed"

            data = response.json()
            tti_model_instance.sd_api_response = data
            tti_model_instance.save()

            for image in data["artifacts"]:
                img_binary_data = base64.b64decode(image["base64"])
                img_file = io.BytesIO(img_binary_data)

            resp = self.s3.upload(
                img_file, "image/png", f"{tti_model_instance.uuid}.png"
            )

            if resp:
                tti_model_instance.status = "completed"
                gen_image_s3_url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{tti_model_instance.uuid}.png"
                tti_model_instance.image_url = gen_image_s3_url
                tti_model_instance.save()
        except Exception as e:
            tti_model_instance.status = "failed"
            tti_model_instance.exception = str(e)
            tti_model_instance.save()
            return "process_sd_task_failed"

        return "process_sd_task_done"


celery_app.register_task(SdTasks())
