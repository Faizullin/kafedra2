from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class AddressConfig(LmsConfig):
    label = "address"
    name = "lms.apps.address"
    verbose_name = _("Address")
