from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils.models import AbstractTimestampedModel, models

UserModel = get_user_model()


class Review(AbstractTimestampedModel):
    author = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return '[{}] {} review for {}'.format(self.pk, self.author, self.content_object)
