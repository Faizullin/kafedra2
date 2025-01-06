from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Review


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    pass
