from django.forms import ModelChoiceField

from .widgets import ThumbnailAttachmentWidget
from lms.core.loading import get_model

Attachment = get_model("attachments", "Attachment")

class ThumbnailAttachmentField(ModelChoiceField):
    widget = ThumbnailAttachmentWidget

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Attachment.objects.all()
        super().__init__(*args, **kwargs)
