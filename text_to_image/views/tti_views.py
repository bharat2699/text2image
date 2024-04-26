from common.utilities.api.base_api_view import BaseAPIView
from common.utilities.api.custom_user_rate_throttle import CustomUserRateThrottle
from common.utilities.decorators.validate_request import validate_request
from text_to_image.serializers import TtiRequestSerializer, TtiResponseSerializer
from text_to_image.services.tti_services import TtiServices


class TtiViews(BaseAPIView):
    throttle_classes = [CustomUserRateThrottle]

    def __init__(self):
        self.service = TtiServices()

    @validate_request(TtiRequestSerializer)
    def post(self, request, data, *args):
        service_data = self.service.post_service(request, data)
        response_data = service_data.get("response_data")
        status_code = service_data.get("code")
        return self.success(response_data, status_code)

    @validate_request(TtiResponseSerializer)
    def get(self, request, data, *args):
        service_data = self.service.get_service(request, data)
        response_data = service_data.get("response_data")
        status_code = service_data.get("code")
        return self.success(response_data, status_code)
