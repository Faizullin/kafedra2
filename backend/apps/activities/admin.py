from .models import ActivityLog
from utils.admin import admin, BaseAdmin


@admin.register(ActivityLog)
class ProfessorAdmin(BaseAdmin):
    pass
