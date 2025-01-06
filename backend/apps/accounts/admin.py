from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Student, UserModel, Professor, UserProfile


class UserAdmin(BaseAdmin):
    list_display = [
        "get_full_name",
        "username",
        "email",
        "is_active",
        "is_student",
        "is_staff",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
    ]

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"


admin.site.register(UserModel, UserAdmin)


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    pass


@admin.register(Professor)
class ProfessorAdmin(BaseAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    pass
