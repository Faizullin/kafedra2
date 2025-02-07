from django.utils.translation import gettext_lazy as _

from utils.models import models, AbstractTimestampedModel


class MultipleChoiceOptions(AbstractTimestampedModel):
    question = models.ForeignKey(
        "quiz.Question",
        on_delete=models.CASCADE,
        related_name="multiple_choice_option",
        verbose_name=_("Question")
    )
    single = models.BooleanField(
        default=False,
        help_text="If False, it's multiple response (checkboxes). Otherwise, it is radio buttons."
    )
    shuffle_answers = models.BooleanField(
        default=True,
        help_text="Whether the choices can be randomly shuffled."
    )
    correct_feedback = models.TextField(
        help_text="Feedback shown for any correct response."
    )
    partially_correct_feedback = models.TextField(
        help_text="Feedback shown for any partially correct response."
    )
    incorrect_feedback = models.TextField(
        help_text="Feedback shown for any incorrect response."
    )
    answer_numbering = models.CharField(
        max_length=10,
        default="abc",
        help_text="Indicates how and whether the choices should be numbered."
    )
    show_num_correct = models.BooleanField(
        default=False,
        help_text="If True, tells how many choices were correct when partially correct."
    )

    class Meta:
        verbose_name = _("Multiple Choice Option")
        verbose_name_plural = _("Multiple Choice Options")

    def __str__(self):
        return f"Multiple Choice Options for {self.question.title}"
