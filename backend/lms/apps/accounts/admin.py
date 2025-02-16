from lms.core.compat import get_user_model
from lms.core.loading import get_model
from utils.admin import BaseAdmin, admin

UserModel = get_user_model()
Student = get_model("accounts", "Student")
Professor = get_model("accounts", "Professor")
UserProfile = get_model("accounts", "UserProfile")

# admin.site.unregister(UserModel)


@admin.register(UserModel)
class UpdatedUserAdmin(BaseAdmin):
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
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
