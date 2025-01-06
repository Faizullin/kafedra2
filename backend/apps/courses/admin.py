from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Program, Course, Upload


@admin.register(Program)
class ProgramAdmin(BaseAdmin):
    pass


@admin.register(Course)
class CourseAdmin(BaseAdmin):
    pass


@admin.register(Upload)
class UploadAdmin(BaseAdmin):
    pass
