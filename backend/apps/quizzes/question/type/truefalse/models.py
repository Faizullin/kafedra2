from django.utils.translation import gettext_lazy as _

from utils.models import models, AbstractTimestampedModel


# class MatchOptions(AbstractTimestampedModel):
#     question = models.OneToOneField(
#         'quiz.Question',
#         on_delete=models.CASCADE,
#         related_name='match_option',
#         verbose_name=_("Question")
#     )
#     shuffle_answers = models.BooleanField(
#         default=True,
#         help_text="Whether the choices can be randomly shuffled."
#     )
#     correct_feedback = models.TextField(
#         help_text="Feedback shown for any correct response."
#     )
#     correct_feedback_format = models.PositiveSmallIntegerField(
#         default=0,
#         help_text="Format of the correct feedback."
#     )
#     partially_correct_feedback = models.TextField(
#         help_text="Feedback shown for any partially correct response."
#     )
#     partially_correct_feedback_format = models.PositiveSmallIntegerField(
#         default=0,
#         help_text="Format of the partially correct feedback."
#     )
#     incorrect_feedback = models.TextField(
#         help_text="Feedback shown for any incorrect response."
#     )
#     incorrect_feedback_format = models.PositiveSmallIntegerField(
#         default=0,
#         help_text="Format of the incorrect feedback."
#     )
#     show_num_correct = models.BooleanField(
#         default=False,
#         help_text="If True, indicates how many choices were correct when partially correct."
#     )
#
#     class Meta:
#         verbose_name = _("Match Option")
#         verbose_name_plural = _("Match Options")
#
#     def __str__(self):
#         return f"Match Options for {self.question.title}"
#
#
# class MatchSubquestion(models.Model):
#     question = models.ForeignKey(
#         'quiz.Question',
#         on_delete=models.CASCADE,
#         related_name='match_subquestions',
#         verbose_name="Question",
#     )
#     question_text = models.TextField(
#         help_text="Text of the subquestion."
#     )
#     answer_text = models.CharField(
#         max_length=255,
#         help_text="Text of the answer corresponding to the subquestion."
#     )
#
#     class Meta:
#         verbose_name = _("Match Subquestion")
#         verbose_name_plural = _("Match Subquestions")
#
#     def __str__(self):
#         return f"Subquestion: {self.question_text} (Answer: {self.answer_text})"
#


class TrueFalseOptions(AbstractTimestampedModel):
    question  = models.OneToOneField(
        'quiz.Question',
        on_delete=models.CASCADE,
        related_name='true_false_option',
        verbose_name=_("Question")
    )
    true_answer = models.ForeignKey("quiz.QuestionAnswer", on_delete=models.CASCADE, related_name='true_option')
    false_answer = models.ForeignKey("quiz.QuestionAnswer", on_delete=models.CASCADE, related_name='false_option')

    class Meta:
        verbose_name = _("True/False Option")
        verbose_name_plural = _("True/False Options")

    def __str__(self):
        return f"True/False Options for {self.question.title}"