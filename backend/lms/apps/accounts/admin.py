from django.contrib import admin

from lms.core.compat import get_user_model


class UserAdmin(admin.ModelAdmin):
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


admin.site.register(get_user_model(), UserAdmin)
