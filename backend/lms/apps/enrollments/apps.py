from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class EnrollmentsConfig(LmsConfig):
    label = "enrollments"
    name = "lms.apps.enrollments"
    verbose_name = _("Enrollments")

    namespace = "enrollments"
