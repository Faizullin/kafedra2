from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class PartnerConfig(LmsConfig):
    label = "partner"
    name = "lms.apps.partner"
    verbose_name = _("Partner")

    # pylint: disable=unused-import
    def ready(self):
        from . import receivers
