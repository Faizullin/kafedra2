from django.contrib.auth import get_user_model

from apps.courses.models import Course
from utils.models import AbstractTimestampedModel, models

UserModel = get_user_model()


class Assignment(AbstractTimestampedModel):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
   title = models.CharField(max_length=200)
   description = models.TextField(help_text="Details about the assignment.")
   due_date = models.DateField()
   submission_requirements = models.TextField(help_text="Requirements for submission.", blank=True)

   owner = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.SET_NULL)