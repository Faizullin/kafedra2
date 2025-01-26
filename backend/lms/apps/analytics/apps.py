from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class AnalyticsConfig(LmsConfig):
    label = "analytics"
    name = "lms.apps.analytics"
    verbose_name = _("Analytics")

    # pylint: disable=unused-import
    def ready(self):
        from . import receivers
