from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import AbstractTimestampedModel


class CurrencyField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', _("Currency"))
        kwargs['max_length'] = 3
        super(CurrencyField, self).__init__(*args, **kwargs)


class LMSPayment(AbstractTimestampedModel):
    member = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_("Member"))
    billing_name = models.CharField(max_length=255, verbose_name=_("Billing Name"))
    # source = models.ForeignKey('LMSSource', on_delete=models.CASCADE, verbose_name=_("Source"))
    payment_for_document_type = models.CharField(max_length=50, choices=[('LMS Course', _('LMS Course')),
                                                                         ('LMS Batch', _('LMS Batch'))],
                                                 verbose_name=_("Payment for Document Type"))
    payment_for_document = models.CharField(max_length=255, verbose_name=_("Payment for Document"))
    payment_received = models.BooleanField(default=False, verbose_name=_("Payment Received"))
    payment_for_certificate = models.BooleanField(default=False, verbose_name=_("Payment for Certificate"))
    currency = CurrencyField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    amount_with_gst = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount with GST"), null=True,
                                          blank=True)
    order_id = models.CharField(max_length=255, verbose_name=_("Order ID"))
    payment_id = models.CharField(max_length=255, verbose_name=_("Payment ID"))
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name=_("Address"))
    gstin = models.CharField(max_length=255, verbose_name=_("GSTIN"))
    pan = models.CharField(max_length=255, verbose_name=_("PAN"))

    class Meta:
        verbose_name = _("LMS Payment")
        verbose_name_plural = _("LMS Payments")
