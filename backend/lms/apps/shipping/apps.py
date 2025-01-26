from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class ShippingConfig(LmsConfig):
    label = "shipping"
    name = "lms.apps.shipping"
    verbose_name = _("Shipping")
