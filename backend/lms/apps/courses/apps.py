from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class CoursesConfig(LmsConfig):
    label = "courses"
    name = "lms.apps.courses"
    verbose_name = _("Courses")

    namespace = "courses"
