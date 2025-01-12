from rest_framework import serializers

from apps.attachments.models import Attachment


class AttachmentActionSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    attachment_type = serializers.ChoiceField(choices=[('thumbnail_image', 'Thumbnail'), ('file', 'File')])
    to_model_field_name = serializers.CharField(required=False, default=None)
    action = serializers.CharField()
    obj_id = serializers.PrimaryKeyRelatedField(
        queryset=Attachment.objects.all(),
    )

