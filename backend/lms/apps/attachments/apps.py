from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from lms.core.application import LmsConfig


class AttachmentConfig(LmsConfig):
    label = "attachments"
    name = "lms.apps.attachments"
    verbose_name = _("Attachment")
    
    def ready(self) -> None:
        import lms.apps.attachments.signals # noqa
        return super().ready()