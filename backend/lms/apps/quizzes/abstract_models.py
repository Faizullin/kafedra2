from django.db import models
from django.utils.translation import gettext_lazy as _

from lms.apps.courses.models import RelatedCourseField
from lms.core.compat import get_user_model
from lms.core.loading import get_model, get_class
from lms.models.fields import AuthorField
from utils.models import AbstractTimestampedModel

PublicationStatus = get_class("posts.models", "PublicationStatus")
Category = get_model("posts", "Category")
UserModel = get_user_model()
QUESTION_CATEGORY_TERM = "question_category"


class AbstractLMSAssessment(AbstractTimestampedModel):
    assessment_type = models.ForeignKey(
        'DocType', on_delete=models.CASCADE, verbose_name=_("Assessment Type")
    )
    assessment_name = models.CharField(max_length=255, verbose_name=_("Assessment Name"))

    class Meta:
        abstract = True
        verbose_name = _("LMS Assessment")
        verbose_name_plural = _("LMS Assessments")


class AbstractLMSQuestionGroup(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    quiz = models.ForeignKey("LMSQuiz", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.pk}] {self.title}"


class AbstractLMSQuiz(AbstractTimestampedModel):
    title = models.CharField(max_length=255, unique=True, verbose_name=_("Title"))
    max_attempts = models.IntegerField(default=0, verbose_name=_("Max Attempts"))
    show_answers = models.BooleanField(default=True, verbose_name=_("Show Answers"))
    show_submission_history = models.BooleanField(default=False, verbose_name=_("Show Submission History"))
    total_marks = models.IntegerField(default=0, verbose_name=_("Total Marks"))
    passing_percentage = models.IntegerField(default=0, verbose_name=_("Passing Percentage"))
    duration = models.IntegerField(verbose_name=_("Duration (in minutes)"), null=True, blank=True)
    shuffle_questions = models.BooleanField(default=False, verbose_name=_("Shuffle Questions"))
    limit_questions_to = models.IntegerField(verbose_name=_("Limit Questions To"), null=True, blank=True)
    lesson = models.ForeignKey(
        'CourseLesson', on_delete=models.SET_NULL, verbose_name=_("Lesson"), null=True, blank=True
    )
    course = RelatedCourseField()
    publication_status = models.IntegerField(
        choices=PublicationStatus.choices, default=PublicationStatus.DRAFT
    )
    author = AuthorField(related_name="quizzes")

    class Meta:
        abstract = True
        verbose_name = _("LMS Quiz")
        verbose_name_plural = _("LMS Quizzes")


class AbstractLMSQuizQuestion(AbstractTimestampedModel):
    title = models.CharField(max_length=200)
    text = models.TextField()
    group = models.ForeignKey(
        "LMSQuestionGroup", null=True, blank=True, on_delete=models.SET_NULL, related_name="questions"
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'term': QUESTION_CATEGORY_TERM}
    )
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    default_grade = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    question_type = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("LMS Quiz Question")
        verbose_name_plural = _("LMS Quiz Questions")


class AbstractLMSQuestionAnswer(AbstractTimestampedModel):
    question = models.ForeignKey("LMSQuizQuestion", on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField(_("Answer"))
    fraction = models.IntegerField(_("Fraction"))
    feedback = models.TextField(_("Feedback"))

    class Meta:
        abstract = True
        verbose_name = _("Question answer")
        verbose_name_plural = _("Question answers")

    def __str__(self):
        return f"[{self.pk}] for {self.question}"


class AbstractLMSQuizResult(AbstractTimestampedModel):
    answer = models.TextField(verbose_name=_("Users Response"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))
    question = models.ForeignKey("LMSQuizQuestion", on_delete=models.CASCADE, verbose_name=_("Question"))
    marks = models.IntegerField(verbose_name=_("Marks"))
    marks_out_of = models.IntegerField(verbose_name=_("Marks out of"))

    class Meta:
        abstract = True
        verbose_name = _("LMS Quiz Result")
        verbose_name_plural = _("LMS Quiz Results")


class AbstractLMSQuizSubmission(AbstractTimestampedModel):
    quiz = models.ForeignKey("LMSQuiz", on_delete=models.CASCADE, verbose_name=_("Quiz"))
    quiz_title = models.CharField(max_length=255, verbose_name=_("Quiz Title"))
    course = RelatedCourseField()
    member = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    score = models.IntegerField(verbose_name=_("Score"))
    score_out_of = models.IntegerField(verbose_name=_("Score Out Of"))
    percentage = models.IntegerField(verbose_name=_("Percentage"))
    passing_percentage = models.IntegerField(verbose_name=_("Passing Percentage"))
    result = models.ManyToManyField("LMSQuizResult", verbose_name=_("Result"))

    class Meta:
        abstract = True
        verbose_name = _("LMS Quiz Submission")
        verbose_name_plural = _("LMS Quiz Submissions")
