from lms.core.loading import get_model
from utils.admin import BaseAdmin, admin


@admin.register(get_model("attachments", "Attachment"))
class AttachmentAdmin(BaseAdmin):
    pass
