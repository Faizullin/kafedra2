from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class QuizConfig(LmsConfig):
    label = "quiz"
    name = "apps.quiz"
    verbose_name = _("Quiz")
    namespace = "quiz"
