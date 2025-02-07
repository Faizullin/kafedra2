from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarConfig


class ActivityLogsConfig(OscarConfig):
    label = "activity_logs"
    name = "apps.activity_logs"
    verbose_name = _("Quiz")
    namespace = "activity_logs"
