from rest_framework import serializers
from utils.serializers import TimestampedSerializer
from apps.attachments.models import Attachment


class AttachmentSerializer(TimestampedSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attachment
        fields = ('id', 'name', 'extension', 'size', 'url',)
        read_only_fields = ('id', 'name', 'extension', 'size')

    def get_url(self, obj: Attachment):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if obj.file else ""