from lms.apps.quizzes.abstract_models import (
    AbstractLMSAssessment,
    AbstractLMSQuestionGroup,
    AbstractLMSQuiz,
    AbstractLMSQuizQuestion,
    AbstractLMSQuestionAnswer,
    AbstractLMSQuizResult,
    AbstractLMSQuizSubmission,
    models,
    _,
)


class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = "MC", _("Multiple Choice")
    TRUE_FALSE = "TF", _("True or False")
    SHORT_ANSWER = "SA", _("Short Answer")
    MATCHING = "MT", _("Matching")
    ESSAY = "ES", _("Essay")
    NUMERIC = "NU", _("Numeric")


class Assessment(AbstractLMSAssessment):
    pass


class QuestionGroup(AbstractLMSQuestionGroup):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    quiz = models.ForeignKey("Quiz", blank=True, null=True, on_delete=models.SET_NULL)


class Quiz(AbstractLMSQuiz):
    pass


class QuizQuestion(AbstractLMSQuizQuestion):
    question_type = models.CharField(max_length=4, choices=QuestionType.choices, null=True, blank=True)
    group = models.ForeignKey(
        "QuestionGroup", null=True, blank=True, on_delete=models.SET_NULL, related_name="questions"
    )


class QuestionAnswer(AbstractLMSQuestionAnswer):
    question = models.ForeignKey("QuizQuestion", on_delete=models.CASCADE, related_name="answers")


class QuizResult(AbstractLMSQuizResult):
    question = models.ForeignKey("QuizQuestion", on_delete=models.CASCADE, verbose_name=_("Question"))


class QuizSubmission(AbstractLMSQuizSubmission):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, verbose_name=_("Quiz"))


from .question.type.choice.models import * # noqa