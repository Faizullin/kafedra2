from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin):
    pass
