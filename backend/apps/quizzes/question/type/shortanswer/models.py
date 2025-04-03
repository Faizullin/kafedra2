from django.utils.translation import gettext_lazy as _

from utils.models import models, AbstractTimestampedModel


class ShortAnswerOptions(AbstractTimestampedModel):
    question = models.OneToOneField(
        'quiz.Question',
        on_delete=models.CASCADE,
        related_name='short_answer_option',
        verbose_name=_("Question"),
        help_text="Foreign key references the base question model."
    )
    use_case = models.BooleanField(
        default=False,
        help_text="Whether answers are matched case-sensitively."
    )

    class Meta:
        verbose_name = _("Short Answer Option")
        verbose_name_plural = _("Short Answer Options")

    def __str__(self):
        return f"Short Answer Options for {self.question.title}"
