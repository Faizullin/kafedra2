from django.contrib import admin

from utils.admin import BaseAdmin
from .models import (
    Certification,
    LMSBadge,
    LMSBadgeAssignment,
    LMSCertificate,
    LMSCertificateEvaluation,
    LMSCertificateRequest,

)


@admin.register(Certification)
class CertificationAdmin(BaseAdmin):
    pass


@admin.register(LMSBadge)
class LMSBadgeAdmin(BaseAdmin):
    pass


@admin.register(LMSBadgeAssignment)
class LMSBadgeAssignmentAdmin(BaseAdmin):
    pass


@admin.register(LMSCertificate)
class LMSCertificateAdmin(BaseAdmin):
    pass


@admin.register(LMSCertificateEvaluation)
class LMSCertificateEvaluationAdmin(BaseAdmin):
    pass


@admin.register(LMSCertificateRequest)
class LMSCertificateRequestAdmin(BaseAdmin):
    pass
