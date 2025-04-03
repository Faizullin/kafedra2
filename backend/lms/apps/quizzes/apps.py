from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class QuizzesConfig(LmsConfig):
    label = "quizzes"
    name = "lms.apps.quizzes"
    verbose_name = _("Quizzes")

    namespace = "quizzes"
