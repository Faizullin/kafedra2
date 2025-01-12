import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.attachments.utils import get_default_upload_file_name
from utils.models import AbstractTimestampedModel


class AbstractFileModel(models.Model):
    name = models.CharField(_("Name"), blank=True, max_length=100)
    extension = models.CharField(_("Extension"), blank=True, max_length=100)
    alt = models.CharField(_("Alt"), blank=True, max_length=255)
    url = models.URLField(_("URL"), blank=True, max_length=255)
    size = models.CharField(_("Size"), blank=True, max_length=100)
    file_type = models.CharField(_("File Type"), default="file", max_length=20)
    parent = models.BigIntegerField(_("Parent"), blank=True, null=True)
    file = models.FileField(_("File"), upload_to=get_default_upload_file_name, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-id",)

    def __str__(self):
        return self.name

    def get_alt(self):
        if self.alt:
            return self.alt
        return self.name


class Attachment(AbstractFileModel, AbstractTimestampedModel):
    attachment_type = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True, )
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs) -> None:
        if self.file:
            self.name = self.file.name
            self.extension = os.path.splitext(self.name)[1]
            self.size = self.file.size
        super().save(*args, **kwargs)
