from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from lms.core.compat import get_user_model
from lms.core.loading import get_model
from utils.models import AbstractTimestampedModel, AbstractMetaModel, AbstractSlugModel

Attachment = get_model("attachments", "Attachment")
UserModel = get_user_model()


class PublicationStatus(models.IntegerChoices):
    DRAFT = 0, "Draft"
    PUBLISH = 1, "Publish"


class Category(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), max_length=1023)
    term = models.CharField(max_length=50, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}) {}'.format(self.pk, self.title)


class Tag(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), max_length=1023)
    term = models.CharField(max_length=50, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}) {}'.format(self.pk, self.title)


class Post(AbstractTimestampedModel, AbstractMetaModel, AbstractSlugModel, SoftDeleteModel):
    title = models.CharField(_("Title"), max_length=200)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    publication_status = models.IntegerField(
        choices=PublicationStatus.choices, default=PublicationStatus.DRAFT)
    post_type = models.CharField(_("Post Type"), max_length=20)

    attachments = GenericRelation(Attachment)
    thumbnail = models.ForeignKey(
        Attachment, null=True, blank=True, on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}) {}'.format(self.pk, self.title)
