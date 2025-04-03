from django.utils.translation import gettext_lazy as _

from lms.apps.courses.models import RelatedCourseField, RelatedCohortField
from lms.core.compat import get_user_model
from lms.core.loading import get_model
from utils.models import AbstractTimestampedModel, models


LMSCertificate = get_model('certifications', 'LMSCertificate')
UserModel = get_user_model()


class CohortJoinRequest(AbstractTimestampedModel):
    cohort = RelatedCohortField()
    subgroup = models.ForeignKey('CohortSubgroup', on_delete=models.CASCADE, verbose_name=_("Subgroup"))
    email = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("E-Mail"))
    status = models.CharField(max_length=50, choices=[('Pending', _('Pending')), ('Accepted', _('Accepted')),
                                                      ('Rejected', _('Rejected'))], default='Pending',
                              verbose_name=_("Status"))

    class Meta:
        verbose_name = _("Cohort Join Request")
        verbose_name_plural = _("Cohort Join Requests")


class CohortMentor(AbstractTimestampedModel):
    cohort = RelatedCohortField()
    email = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("E-mail"))
    subgroup = models.ForeignKey('CohortSubgroup', on_delete=models.CASCADE, verbose_name=_("Primary Subgroup"))
    course = RelatedCourseField()

    class Meta:
        verbose_name = _("Cohort Mentor")
        verbose_name_plural = _("Cohort Mentors")


class CohortStaff(AbstractTimestampedModel):
    cohort = RelatedCohortField()
    email = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("User"))
    role = models.CharField(max_length=50,
                            choices=[('Admin', _('Admin')), ('Manager', _('Manager')), ('Staff', _('Staff'))],
                            verbose_name=_("Role"))
    course = RelatedCourseField()

    class Meta:
        verbose_name = _("Cohort Staff")
        verbose_name_plural = _("Cohort Staff")


class LMSEnrollment(AbstractTimestampedModel):
    # batch_old = models.ForeignKey('LMSBatchOld', on_delete=models.CASCADE, verbose_name=_("Batch Old"))
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_type = models.CharField(max_length=50,
                                   choices=[('Student', _('Student')), ('Mentor', _('Mentor')), ('Staff', _('Staff'))],
                                   default='Student', verbose_name=_("Member Type"))
    role = models.CharField(max_length=50, choices=[('Member', _('Member')), ('Admin', _('Admin'))], default='Member',
                            verbose_name=_("Role"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    course = RelatedCohortField()
    current_lesson = models.ForeignKey('CourseLesson', on_delete=models.CASCADE, verbose_name=_("Current Lesson"))
    member_username = models.CharField(max_length=255, verbose_name=_("Member Username"))
    progress = models.FloatField(verbose_name=_("Progress"))
    cohort = RelatedCohortField()
    subgroup = models.ForeignKey('CohortSubgroup', on_delete=models.CASCADE, verbose_name=_("Subgroup"))
    payment = models.ForeignKey('LMSPayment', on_delete=models.CASCADE, verbose_name=_("Payment"))
    purchased_certificate = models.BooleanField(default=False, verbose_name=_("Purchased Certificate"))
    certificate = models.ForeignKey('LMSCertificate', on_delete=models.CASCADE, verbose_name=_("Certificate"))

    class Meta:
        verbose_name = _("LMS Enrollment")
        verbose_name_plural = _("LMS Enrollments")


class LMSMentorRequest(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    course = RelatedCohortField()
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    status = models.CharField(max_length=50, choices=[('Pending', _('Pending')), ('Approved', _('Approved')),
                                                      ('Rejected', _('Rejected')), ('Withdrawn', _('Withdrawn'))],
                              default='Pending', verbose_name=_("Status"))
    reviewed_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviewed_by',
                                    verbose_name=_("Reviewed By"))
    comments = models.TextField(verbose_name=_("Comments"))

    class Meta:
        verbose_name = _("LMS Mentor Request")
        verbose_name_plural = _("LMS Mentor Requests")


class LMSProgramMember(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    progress = models.IntegerField(default=0, verbose_name=_("Progress"))

    class Meta:
        verbose_name = _("LMS Program Member")
        verbose_name_plural = _("LMS Program Members")
