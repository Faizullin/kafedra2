from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class AssignmentsConfig(LmsConfig):
    label = "assignments"
    name = "lms.apps.assignments"
    verbose_name = _("Assignments")

    namespace = "assignments"
