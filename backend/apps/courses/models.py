from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utils.models import AbstractTimestampedModel, AbstractSlugModel
# project import
from .utils import *
from ..accounts.models import Professor
from ..activities.models import ActivityLog
from ..posts.models import Category

YEARS = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (4, "5"),
    (4, "6"),
)

# LEVEL_COURSE = "Level courses"
BACHELOR_DEGREE = _("Bachelor")
MASTER_DEGREE = _("Master")

LEVEL = (
    # (LEVEL_COURSE, "Level courses"),
    (BACHELOR_DEGREE, _("Bachelor Degree")),
    (MASTER_DEGREE, _("Master Degree")),
)

FIRST = _("First")
SECOND = _("Second")
THIRD = _("Third")

SEMESTER = (
    (FIRST, _("First")),
    (SECOND, _("Second")),
    (THIRD, _("Third")),
)

UserModel = get_user_model()


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

    def __str__(self):
        return '[{}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def is_current_semester(self):

        current_semester = AcademicSemester.objects.get(is_current_semester=True)

        if self.semester == current_semester.semester:
            return True
        else:
            return False


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=_(f"The course '{instance}' has been {verb}."))


@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=_(f"The course '{instance}' has been deleted."))


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
        Before we Save any data in the class room lets check to see if there are open sits

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


# class ClassRoomAllocation(models.Model):
#     lecturer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name=_("allocated_lecturer"),
#     )
#     courses = models.ManyToManyField(ClassRoom, related_name=_("allocated_course"))
#     # session = models.ForeignKey(
#     #     "core.Session", on_delete=models.CASCADE, blank=True, null=True
#     # )
#
#     def __str__(self):
#         return self.lecturer.get_full_name
#
#     def get_absolute_url(self):
#         return reverse("edit_allocated_course", kwargs={"pk": self.pk})


class Upload(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="course_files/",
        help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
        validators=[
            FileExtensionValidator(
                [
                    "pdf",
                    "docx",
                    "doc",
                    "xls",
                    "xlsx",
                    "ppt",
                    "pptx",
                    "zip",
                    "rar",
                    "7zip",
                ]
            )
        ],
    )
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext in ("doc", "docx"):
            return "word"
        elif ext == "pdf":
            return "pdf"
        elif ext in ("xls", "xlsx"):
            return "excel"
        elif ext in ("ppt", "pptx"):
            return "powerpoint"
        elif ext in ("zip", "rar", "7zip"):
            return "archive"

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Upload)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=_(
                f"The file '{instance.title}' has been uploaded to the course '{instance.course}'."
            )
        )
    else:
        ActivityLog.objects.create(
            message=_(
                f"The file '{instance.title}' of the course '{instance.course}' has been updated."
            )
        )


@receiver(post_delete, sender=Upload)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=_(
            f"The file '{instance.title}' of the course '{instance.course}' has been deleted."
        )
    )


class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to="course_videos/",
        help_text=_("Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3"),
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse(
            "video_single", kwargs={"slug": self.course.slug, "video_slug": self.slug}
        )

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)


def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(video_pre_save_receiver, sender=UploadVideo)


@receiver(post_save, sender=UploadVideo)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=_(
                f"The video '{instance.title}' has been uploaded to the course {instance.course}."
            )
        )
    else:
        ActivityLog.objects.create(
            message=_(
                f"The video '{instance.title}' of the course '{instance.course}' has been updated."
            )
        )


@receiver(post_delete, sender=UploadVideo)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=_(
            f"The video '{instance.title}' of the course '{instance.course}' has been deleted."
        )
    )


# class CourseOffer(models.Model):
#     _("""NOTE: Only department head can offer semester courses""")
#
#     dep_head = models.ForeignKey("accounts.DepartmentHead", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "{}".format(self.dep_head)
