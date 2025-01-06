from utils.admin import BaseAdmin, admin
from .models import Lecture, Glossary


@admin.register(Lecture)
class LectureAdmin(BaseAdmin):
    pass


@admin.register(Glossary)
class GlossaryAdmin(BaseAdmin):
    pass
