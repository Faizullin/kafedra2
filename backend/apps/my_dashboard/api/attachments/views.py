from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django_filters import ModelChoiceFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import generics, status, pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.attachments.models import Attachment, models
from .serializers import AttachmentSerializer, AttachmentUploadSerializer, AttachmentActionSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AttachmentListAPIView(generics.ListAPIView):
    serializer_class = AttachmentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name', "id"]
    ordering_fields = ['id', 'created_at', 'updated_at']

    class AttachmentFilter(FilterSet):
        content_type = ModelChoiceFilter(
            field_name='content_type',
            queryset=ContentType.objects.all(),
            to_field_name='model',
            label="Content Type",
        )
        NumberFilter(
            field_name='object_id',
            lookup_expr='exact',
        )

        class Meta:
            model = Attachment
            fields = ['id', 'content_type', 'object_id']

    filterset_class = AttachmentFilter

    def get_queryset(self):
        queryset = Attachment.objects.all()
        return queryset


class AttachmentUploadAPIView(APIView):
    def post(self, request):
        serializer = AttachmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type = serializer.validated_data['content_type']
        object_id = serializer.validated_data['object_id']
        to_model_field_name = serializer.validated_data.get('to_model_field_name', None)

        model_class = content_type.model_class()
        try:
            related_obj = model_class.objects.get(pk=object_id)
        except model_class.DoesNotExist:
            return Response(
                {"error": "The related object does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        related_field = None
        if serializer.validated_data['attachment_type'] == "thumbnail_image":
            if not to_model_field_name:
                return Response({"error": "`to_model_field_name` is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                related_field = model_class._meta.get_field(to_model_field_name)
                if not (isinstance(related_field, models.ForeignKey) and related_field.related_model == Attachment):
                    return Response({"error": "`to_model_field_name` is not correct field"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except FieldDoesNotExist:
                return Response({"error": "`to_model_field_name` is not correct field"},
                                status=status.HTTP_400_BAD_REQUEST)

        attachment_obj = Attachment.objects.create(
            file=serializer.validated_data['file'],
            content_type=serializer.validated_data['content_type'],
            object_id=serializer.validated_data['object_id'],
            attachment_type=serializer.validated_data['attachment_type']
        )
        if related_field is not None:
            setattr(related_obj, related_field.name, attachment_obj)
            related_obj.save()
        return Response(AttachmentSerializer(attachment_obj).data, status=status.HTTP_201_CREATED)


class AttachmentDeleteAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        obj_id = request.data.get("id")
        attachment_obj = get_object_or_404(Attachment, pk=obj_id)
        attachment_obj.delete()
        return Response(
            {"message": "Attachment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AttachmentActionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AttachmentActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = serializer.validated_data['obj_id']
        action = serializer.validated_data.get("action")
        if action not in ['attach_related_single', 'detach_related_single']:
            return Response({"error": "`action` is not a valid action."}, status=status.HTTP_400_BAD_REQUEST)
        content_type = serializer.validated_data['content_type']
        object_id = serializer.validated_data['object_id']
        to_model_field_name = serializer.validated_data.get('to_model_field_name', None)
        model_class = content_type.model_class()
        try:
            related_obj = model_class.objects.get(pk=object_id)
        except model_class.DoesNotExist:
            return Response(
                {"error": "The related object does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "attach_related_single":
            if not to_model_field_name:
                return Response({"error": "`to_model_field_name` is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                related_field = model_class._meta.get_field(to_model_field_name)
                if not (isinstance(related_field, models.ForeignKey) and related_field.related_model == Attachment):
                    return Response({"error": "`to_model_field_name` is not correct field"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except FieldDoesNotExist:
                return Response({"error": "`to_model_field_name` is not correct field"},
                                status=status.HTTP_400_BAD_REQUEST)
            if related_field is not None:
                setattr(related_obj, related_field.name, obj)
                related_obj.save()
        elif action == "detach_related_single":
            if not to_model_field_name:
                return Response({"error": "`to_model_field_name` is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                related_field = model_class._meta.get_field(to_model_field_name)
                if not (isinstance(related_field, models.ForeignKey) and related_field.related_model == Attachment):
                    return Response({"error": "`to_model_field_name` is not correct field"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except FieldDoesNotExist:
                return Response({"error": "`to_model_field_name` is not correct field"},
                                status=status.HTTP_400_BAD_REQUEST)
            if related_field is not None:
                setattr(related_obj, related_field.name, None)
                related_obj.save()

        return Response(
            {"message": "Action done successfully."},
            status=status.HTTP_200_OK,
        )
