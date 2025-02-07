from django.contrib import admin

from lms.core.loading import get_model
from utils.admin import BaseAdmin

Assignment = get_model("assignments", "Assignment")


@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin):
    pass
