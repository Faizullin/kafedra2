from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class VoucherConfig(LmsConfig):
    label = "voucher"
    name = "lms.apps.voucher"
    verbose_name = _("Voucher")

    def ready(self):
        # pylint: disable=unused-import
        from . import receivers
