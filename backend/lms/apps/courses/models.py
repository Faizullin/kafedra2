from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lms.core.compat import get_user_model
from lms.core.loading import get_model, get_class
from utils.models import AbstractTimestampedModel, AbstractSlugModel

UserModel = get_user_model()
Category = get_model("posts", "Category")
PublicationStatus = get_class("posts.models", "PublicationStatus")
Attachment = get_model("attachments", "Attachment")
Professor = get_model("accounts", "Professor")


class Program(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"pk": self.pk})


class AcademicSemester(AbstractTimestampedModel):
    name = models.CharField(max_length=100, null=True)
    days = models.PositiveIntegerField(null=True)
    year = models.PositiveIntegerField(null=True)
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return '[{}] {} days'.format(self.pk, self.days)


class Course(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True, null=True)
    credit = models.IntegerField(null=True, default=0)
    duration_hours = models.PositiveIntegerField(help_text="Estimated time for learning the main parts in hours.")
    duration_weeks = models.PositiveIntegerField(help_text="Duration of the course in weeks.")

    prerequisites = models.TextField(help_text="Requirements for prior subjects or intended audience.")
    keywords = models.TextField(help_text="Comma-separated keywords.")
    abbreviations = models.TextField(help_text="List of abbreviations and their meanings.", blank=True)
    objective = models.TextField(help_text="Purpose or aim of the course.")
    summary = models.TextField(help_text="General summary of the course.", max_length=200, blank=True, null=True)

    semester = models.ForeignKey(AcademicSemester, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(UserModel, null=True, blank=True, related_name='courses', on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    publication_status = models.IntegerField(
        choices=PublicationStatus.choices, default=PublicationStatus.DRAFT)
    attachments = GenericRelation(Attachment)
    thumbnail = models.ForeignKey(
        Attachment, null=True, blank=True, on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '[{}] {}'.format(self.pk, self.title)

    @property
    def is_current_semester(self):

        current_semester = AcademicSemester.objects.get(is_current_semester=True)

        if self.semester == current_semester.semester:
            return True
        else:
            return False


class ClassRoom(models.Model):
    name = models.CharField(max_length=100, null=True)
    # stream = models.ForeignKey(
    #     Stream, on_delete=models.CASCADE, blank=True, related_name="class_stream"
    # )
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True)
    # grade_level = models.ForeignKey(
    #     GradeLevel,
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     help_text="the grade level of the class ie: 'form one is in Grade one' ",
    # )
    capacity = models.IntegerField(
        help_text="Enter total number of sits default is set to 40",
        default=40,
        blank=True,
    )
    occupied_sits = models.IntegerField(blank=True, null=True, default=0)
    semester = models.ForeignKey(AcademicSemester, null=True, blank=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return "{}) {}".format(self.pk, self.name)

    def available_sits(self):
        open_sits = self.capacity - self.occupied_sits
        return open_sits

    def class_status(self):
        # get the percentage of occupied sits
        percentage = (self.occupied_sits / self.capacity) * 100
        return "{}%".format(float(percentage))

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Before we Save any data in the classroom lets check to see if there are open sits

        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if (self.capacity - self.occupied_sits) < 0:
            raise ValueError(
                "all sits in this classroom are occupied try other classes"
            )
        else:
            super(ClassRoom, self).save()


class ClassRoomAllocation(models.Model):
    lecturer = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name=_("allocated_lecturer"),
    )
    rooms = models.ManyToManyField(ClassRoom, blank=True)
    # session = models.ForeignKey(
    #     "core.Session", on_delete=models.CASCADE, blank=True, null=True
    # )

# class CourseOffer(models.Model):
#     _("""NOTE: Only department head can offer semester courses""")
#
#     dep_head = models.ForeignKey("accounts.DepartmentHead", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "{}".format(self.dep_head)
