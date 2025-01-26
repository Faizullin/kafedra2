from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class PaymentConfig(LmsConfig):
    label = "payment"
    name = "lms.apps.payment"
    verbose_name = _("Payment")
