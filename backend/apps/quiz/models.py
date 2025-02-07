from django.utils.translation import gettext_lazy as _

from lms.core.compat import get_user_model
from lms.core.loading import get_model, get_class
from lms.models.fields import AuthorField
from utils.models import AbstractTimestampedModel, models

Course = get_model("courses", "Course")
ClassRoom = get_model("courses", "ClassRoom")
PublicationStatus = get_class("posts.models", "PublicationStatus")
Category = get_model("posts", "Category")

UserModel = get_user_model()

QUESTION_CATEGORY_TERM = "question_category"


class Quiz(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    publication_status = models.IntegerField(
        choices=PublicationStatus.choices, default=PublicationStatus.DRAFT)
    author = AuthorField(related_name="quizzes")

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class QuestionGroup(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    quiz = models.ForeignKey(Quiz, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = "MC", _("Multiple Choice")
    TRUE_FALSE = "TF", _("True or False")
    SHORT_ANSWER = "SA", _("Short Answer")
    MATCHING = "MT", _("Matching")
    ESSAY = "ES", _("Essay")
    NUMERIC = "NU", _("Numeric")


class Question(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    text = models.TextField()
    group = models.ForeignKey(QuestionGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name="questions")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                                 limit_choices_to={'term': QUESTION_CATEGORY_TERM})
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    default_grade = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    question_type = models.CharField(
        max_length=4,
        choices=QuestionType.choices,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)


class QuestionAnswer(AbstractTimestampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField(_("Answer"))
    fraction = models.IntegerField(_("Fraction"))
    feedback = models.TextField(_("Feedback"))

    class Meta:
        verbose_name = _("Question answer")
        verbose_name_plural = _("Question answers")

    def __str__(self):
        return "[{}] for {}".format(self.pk, self.question)


from .question.type.choice.models import *  # noqa
from .question.type.truefalse.models import *  # noqa
from .question.type.shortanswer.models import *  # noqa


class QuestionSession(AbstractTimestampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="sessions")
