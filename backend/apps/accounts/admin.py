from apps.accounts.models import Student, Professor, UserProfile
from lms.apps.accounts.admin import admin, UserAdmin as BaseUserAdmin
from lms.core.compat import get_user_model
from utils.admin import BaseAdmin

UserModel = get_user_model()

admin.site.unregister(UserModel)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    pass


@admin.register(Professor)
class ProfessorAdmin(BaseAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    pass
