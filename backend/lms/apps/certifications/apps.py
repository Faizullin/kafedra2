from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class CertificationsConfig(LmsConfig):
    label = "certifications"
    name = "lms.apps.certifications"
    verbose_name = _("Certifications")

    namespace = "certifications"
