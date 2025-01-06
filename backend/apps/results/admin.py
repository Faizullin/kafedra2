from utils.admin import BaseAdmin, admin
from .models import TakenCourse, Result


@admin.register(TakenCourse)
class TakenCourseAdmin(BaseAdmin):
    list_display = [
        "student",
        "course",
        "assignment",
        "mid_exam",
        "quiz",
        "attendance",
        "final_exam",
        "total",
        "grade",
        "comment",
    ]


@admin.register(Result)
class ResultAdmin(BaseAdmin):
    pass
