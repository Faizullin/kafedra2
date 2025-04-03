from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class CoreConfig(LmsConfig):
    label = "core"
    name = "lms.apps.core"
    verbose_name = _("Core")

    namespace = "core"
