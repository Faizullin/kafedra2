from utils.admin import BaseAdmin, admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(BaseAdmin):
    pass
