from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class OrderConfig(LmsConfig):
    label = "order"
    name = "lms.apps.order"
    verbose_name = _("Order")
