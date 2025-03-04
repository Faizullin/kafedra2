from django.contrib.contenttypes.models import ContentType
from rest_framework import status


class BaseActionException(Exception):
    status = status.HTTP_400_BAD_REQUEST

    def __init__(self, *args):
        super().__init__(*args)


class BaseAction:
    name: str

    def apply(self, request):
        raise BaseActionException("Incorrect action")

    def get_content_obj_data_raw_from_request(self, request):
        content_type = request.data.get('content_type', None)
        object_id = request.data.get('object_id', None)
        return content_type, object_id

    def get_content_type_obj_from_request(self, request):
        content_type, object_id = self.get_content_obj_data_raw_from_request(request)
        if not (content_type and object_id):
            raise BaseActionException("Incorrect params for this action.")
        try:
            content_type = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise BaseActionException("Content type does not exist.")
        model_class = content_type.model_class()
        try:
            related_obj = model_class.objects.get(pk=object_id)
        except model_class.DoesNotExist:
            raise BaseActionException("The related object does not exist")
        return content_type, related_obj
