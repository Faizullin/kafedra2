from django.forms import widgets

from lms.core.loading import get_model

Attachment = get_model("attachments", "Attachment")


class ThumbnailAttachmentWidget(widgets.Widget):
    template_name = 'lms/dashboard/widgets/thumbnail_attachment_widget.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value:
            related_instance_obj = Attachment.objects.get(pk=value)
            context['related_instance_obj'] = related_instance_obj
        return context
