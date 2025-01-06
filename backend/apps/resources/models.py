from django.contrib.contenttypes.fields import GenericRelation

from apps.attachments.models import Attachment
from apps.courses.models import Course
from utils.models import models, AbstractTimestampedModel, AbstractSlugModel


class Glossary(AbstractTimestampedModel):
    term = models.CharField(max_length=100)
    definition = models.TextField()
    language = models.CharField(max_length=50, choices=[
        ('en', 'English'),
        ('ru', 'Russian'),
        ('sk', 'Slovak'),
        ('kz', 'Kazakh'),
    ])  # todo: remove languages

    def __str__(self):
        return "{}). {}".format(self.pk, self.term)


class Lecture(AbstractTimestampedModel, AbstractSlugModel):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name="lectures")
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Detailed content of the lecture.")
    duration_hours = models.PositiveIntegerField(help_text="Estimated time for this lecture in hours.")
    attachments = GenericRelation(Attachment)

    def __str__(self):
        return "{}). {}".format(self.pk, self.title)
