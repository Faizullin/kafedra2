from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.attachments.models import Attachment, models


class ImageUploadAPIView(APIView):
    def post(self, request):
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return Response(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            filename, extension = os.path.splitext(the_file.name)

            if IMAGE_NAME_ORIGINAL is False:
                filename = IMAGE_NAME(filename=filename, file=the_file)

            filename += extension

            upload_path = IMAGE_UPLOAD_PATH

            if IMAGE_UPLOAD_PATH_DATE:
                upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)

            path = storage.save(
                os.path.join(upload_path, filename), the_file
            )
            link = storage.url(path)

            return Response({'success': 1, 'file': {"url": link}})
        return Response({'success': 0})


class ActionException(Exception):
    status = status.HTTP_400_BAD_REQUEST

    def __init__(self, *args):
        super().__init__(*args)


class BaseAction:
    name: str

    def apply(self, request):
        raise ActionException("Incorrect action")

    def get_content_type_obj_from_request(self, request):
        content_type = request.data.get('content_type', None)
        object_id = request.data.get('object_id', None)
        if not (content_type and object_id):
            raise ActionException("Incorrect params for this action.")
        try:
            content_type = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise ActionException("Content type does not exist.")
        model_class = content_type.model_class()
        try:
            related_obj = model_class.objects.get(pk=object_id)
        except model_class.DoesNotExist:
            raise ActionException("The related object does not exist")
        return content_type, related_obj


class UploadImageByFileAction(BaseAction):
    name = "image-upload-by-file"

    def apply(self, request):
        the_file = request.FILES.get('file', None)
        if not the_file:
            raise ActionException(
                "file is required"
            )
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/pjpeg',
            'image/x-png',
            'image/png',
            'image/webp',
            'image/gif',
        ]
        if the_file.content_type not in allowed_types:
            return ActionException(
                'You can only upload images.'
            )
        content_type, related_obj = self.get_content_type_obj_from_request(request)
        attachment_obj = Attachment.objects.create(
            file=the_file,
            content_type=content_type,
            object_id=related_obj.pk,
            attachment_type="content-image"
        )
        return {'success': 1, 'file': {
            "url": attachment_obj.file.url,
        }}


class SaveContentAction(BaseAction):
    name = "save-content"

    def apply(self, request):
        to_model_field_name = request.data.get('to_model_field_name', None)
        if not to_model_field_name:
            raise ActionException("Incorrect params for this action.")
        content = request.data.get('content', None)
        if not content:
            raise ActionException("Incorrect params for this action.")
        content_type, related_obj = self.get_content_type_obj_from_request(request)
        try:
            related_field = related_obj._meta.get_field(to_model_field_name)
            if not (isinstance(related_field, models.TextField)):
                raise ActionException("`to_model_field_name` is not correct field")
        except FieldDoesNotExist:
            raise ActionException("`to_model_field_name` is not correct field")
        if related_field is not None:
            setattr(related_obj, related_field.name, content)
            related_obj.save()
        return {
            "message": "Successfully saved content to {}.".format(related_obj),
        }


class ContentEditorActionAPIView(APIView):
    def post(self, request):
        actions = [
            UploadImageByFileAction(),
            SaveContentAction(),
        ]
        action = request.data.get('action', None)
        if action is None:
            return Response({'success': 0, "message": "`action` is required"}, status=status.HTTP_400_BAD_REQUEST)
        for i in actions:
            if i.name == action:
                try:
                    response = i.apply(request)
                    return Response(response, status=status.HTTP_200_OK)
                except ActionException as e:
                    return Response({'success': 0, 'message': str(e)}, status=e.status)
        return Response({'success': 0, "message": "`action` is invalid"}, status=status.HTTP_400_BAD_REQUEST)
