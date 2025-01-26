from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.courses.models import Course, ClassRoom
from utils.models import AbstractTimestampedModel, models

UserModel = get_user_model()


class Assignment(AbstractTimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    classroom = models.ForeignKey(ClassRoom, blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Details about the assignment.")
    due_date = models.DateField()
    submission_requirements = models.TextField(help_text="Requirements for submission.", blank=True)

    owner = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")

    def __str__(self):
        return "[{}] {}".format(self.pk, self.title)

