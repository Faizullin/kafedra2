from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from utils.models import AbstractTimestampedModel
from .fields import AvatarField, conf


class UserApprovalStatus(models.TextChoices):
    APPROVED = ('approved', 'Approved')
    REJECTED = ('rejected', 'Rejected')
    PENDING = ('pending', 'Pending')


class GenderChoice(models.TextChoices):
    MALE = ('m', _("Male"))
    FEMALE = ('f', _("Female"))


class CustomUser(AbstractUser, SoftDeleteModel):
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

    def get_picture(self):
        try:
            return self.avatar.url
        except:
            no_picture = settings.MEDIA_URL + conf.default_avatar_image
            return no_picture

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    approval_status = models.CharField(
        max_length=10,
        choices=UserApprovalStatus.choices,
        default=UserApprovalStatus.PENDING,
    )
    avatar = AvatarField(null=True, blank=True, )
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

    class Meta:
        ordering = ("-id",)


class Professor(AbstractTimestampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="professor")

    class Meta:
        ordering = ("-id",)
