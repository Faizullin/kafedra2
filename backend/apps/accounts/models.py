from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from PIL import Image
from django_softdelete.models import SoftDeleteModel

# from apps.courses.models import Program
from utils.models import AbstractTimestampedModel
from .fields import AvatarField, conf
from .validators import ASCIIUsernameValidator


# LEVEL_COURSE = "Level courses"
BACHELOR_DEGREE = _("Bachelor")
MASTER_DEGREE = _("Master")

LEVEL = (
    # (LEVEL_COURSE, "Level courses"),
    (BACHELOR_DEGREE, _("Bachelor Degree")),
    (MASTER_DEGREE, _("Master Degree")),
)

FATHER = _("Father")
MOTHER = _("Mother")
BROTHER = _("Brother")
SISTER = _("Sister")
GRAND_MOTHER = _("Grand mother")
GRAND_FATHER = _("Grand father")
OTHER = _("Other")

RELATION_SHIP = (
    (FATHER, _("Father")),
    (MOTHER, _("Mother")),
    (BROTHER, _("Brother")),
    (SISTER, _("Sister")),
    (GRAND_MOTHER, _("Grand mother")),
    (GRAND_FATHER, _("Grand father")),
    (OTHER, _("Other")),
)


class UserApprovalStatus(models.TextChoices):
    APPROVED = ('approved', 'Approved')
    REJECTED = ('rejected', 'Rejected')
    PENDING = ('pending', 'Pending')


class GenderChoice(models.TextChoices):
    MALE = ('m', _("Male"))
    FEMALE = ('f', _("Female"))


class CustomUser(AbstractUser, SoftDeleteModel):
    # is_student = models.BooleanField(default=False)
    # is_lecturer = models.BooleanField(default=False)
    # is_parent = models.BooleanField(default=False)
    # is_dep_head = models.BooleanField(default=False)
    # gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    # phone = models.CharField(max_length=60, blank=True, null=True)
    # address = models.CharField(max_length=60, blank=True, null=True)
    # picture = models.ImageField(
    #     upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    # )
    # email = models.EmailField(blank=True, null=True)
    #
    # username_validator = ASCIIUsernameValidator()
    #
    # objects = CustomUserManager()

    class Meta:
        ordering = ("-date_joined",)

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)

    # @property
    # def get_user_role(self):
    #     if self.is_superuser:
    #         role = _("Admin")
    #     elif self.is_student:
    #         role = _("Student")
    #     elif self.is_lecturer:
    #         role = _("Lecturer")
    #     elif self.is_parent:
    #         role = _("Parent")
    #
    #     return role

    def get_picture(self):
        try:
            return self.avatar.url
        except:
            no_picture = settings.MEDIA_URL + conf.default_avatar_image
            return no_picture

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     try:
    #         img = Image.open(self.picture.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.picture.path)
    #     except:
    #         pass


    approval_status = models.CharField(
        max_length=10,
        choices=UserApprovalStatus.choices,
        default=UserApprovalStatus.PENDING,
    )
    avatar = AvatarField(null=True, blank=True,)
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        print("delete", self.avatar.path, conf.default_avatar_image)
        if self.avatar.path != conf.default_avatar_image:
            self.avatar.delete()
        super().delete(*args, **kwargs)


UserModel = CustomUser


class UserProfile(AbstractTimestampedModel, SoftDeleteModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile', db_index=True)
    bio = models.TextField(blank=True)
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_private = models.BooleanField(default=False)
    gender = models.CharField(
        choices=GenderChoice.choices,
        null=True,
        blank=True,
        max_length=1,
    )


#
# class StudentManager(models.Manager):
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query is not None:
#             or_lookup = Q(level__icontains=query) | Q(program__icontains=query)
#             qs = qs.filter(
#                 or_lookup
#             ).distinct()  # distinct() is often necessary with Q lookups
#         return qs


class Student(AbstractTimestampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    # id_number = models.CharField(max_length=20, unique=True, blank=True)
#     level = models.CharField(max_length=25, choices=LEVEL, null=True)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
#
#     objects = StudentManager()
#
    class Meta:
        ordering = ("-id",)
#
#     def __str__(self):
#         return self.student.get_full_name
#
#     @classmethod
#     def get_gender_count(cls):
#         males_count = Student.objects.filter(student__gender="M").count()
#         females_count = Student.objects.filter(student__gender="F").count()
#
#         return {"M": males_count, "F": females_count}
#
#     def get_absolute_url(self):
#         return reverse("profile_single", kwargs={"id": self.id})
#
#     def delete(self, *args, **kwargs):
#         self.student.delete()
#         super().delete(*args, **kwargs)


class Professor(AbstractTimestampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="professor")
    
    class Meta:
        ordering = ("-id",)


# class Parent(models.Model):
#     """
#     Connect student with their parent, parents can
#     only view their connected students information
#     """
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
#     first_name = models.CharField(max_length=120)
#     last_name = models.CharField(max_length=120)
#     phone = models.CharField(max_length=60, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#
#     # What is the relationship between the student and
#     # the parent (i.e. father, mother, brother, sister)
#     relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)
#
#     class Meta:
#         ordering = ("-user__date_joined",)
#
#     def __str__(self):
#         return self.user.username
#
#
# class DepartmentHead(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         ordering = ("-user__date_joined",)
#
#     def __str__(self):
#         return "{}".format(self.user)
