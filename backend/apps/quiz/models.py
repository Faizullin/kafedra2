from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.courses.models import Course, ClassRoom
from apps.posts.models import PublicationStatus
from utils.models import AbstractTimestampedModel, models

UserModel = get_user_model()


class Quiz(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    publication_status = models.IntegerField(
        choices=PublicationStatus.choices, default=PublicationStatus.DRAFT)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class QuestionGroup(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class Question(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    text = models.TextField()
    group = models.ForeignKey(QuestionGroup, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class QuestionAnswer(AbstractTimestampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()

    class Meta:
        verbose_name = _("Question answer")
        verbose_name_plural = _("Question answers")

    def __str__(self):
        return "[{}] for {}".format(self.pk, self.question)
