from django.contrib import admin

from lms.core.loading import get_model
from utils.admin import BaseAdmin


@admin.register(get_model("courses", "Program"))
class ProgramAdmin(BaseAdmin):
    pass


@admin.register(get_model("courses", "Course"))
class CourseAdmin(BaseAdmin):
    pass


@admin.register(get_model("courses", "ClassRoom"))
class ClassRoomAdminAdmin(BaseAdmin):
    pass


@admin.register(get_model("courses", "ClassRoomAllocation"))
class ClassRoomAllocationAdminAdmin(BaseAdmin):
    pass
