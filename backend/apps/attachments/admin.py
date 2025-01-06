from django.contrib import admin
from .models import Attachment
from utils.admin import BaseAdmin


@admin.register(Attachment)
class AttachmentAdmin(BaseAdmin):
    pass