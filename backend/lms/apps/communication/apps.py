from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class CommunicationConfig(LmsConfig):
    label = "communication"
    name = "lms.apps.communication"
    verbose_name = _("Communication")
