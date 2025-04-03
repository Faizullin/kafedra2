from django.utils.translation import gettext_lazy as _

from lms.apps.core.models import EventChoices, DayChoices, StatusChoices
from lms.apps.courses.models import RelatedCourseField
from lms.core.compat import get_user_model
from lms.core.loading import get_model
from utils.models import models, AbstractSlugModel, AbstractTimestampedModel

UserModel = get_user_model()
LMSBatch = get_model('courses', 'LMSBatch')


class Certification(AbstractTimestampedModel):
    certification_name = models.CharField(max_length=255, verbose_name=_("Certification Name"))
    organization = models.CharField(max_length=255, verbose_name=_("Organization"))
    description = models.TextField(verbose_name=_("Description"))
    expire = models.BooleanField(default=False, verbose_name=_("This certificate does not expire"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiration_date = models.DateField(verbose_name=_("Expiration Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Certification")
        verbose_name_plural = _("Certifications")


class LMSBadge(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=255, unique=True, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to='badge_images/', verbose_name=_("Image"))
    grant_only_once = models.BooleanField(default=False, verbose_name=_("Grant only once"))
    event = models.CharField(max_length=50, choices=EventChoices.choices, verbose_name=_("Event"))
    # reference_doctype = models.ForeignKey('DocType', on_delete=models.CASCADE,
    #                                       verbose_name=_("Reference Document Type"))
    user_field = models.CharField(max_length=255, verbose_name=_("User Field"))
    field_to_check = models.CharField(max_length=255, verbose_name=_("Field To Check"), null=True, blank=True)
    condition = models.TextField(verbose_name=_("Condition"), null=True, blank=True)
    enabled = models.BooleanField(default=True, verbose_name=_("Enabled"))

    class Meta:
        verbose_name = _("LMS Badge")
        verbose_name_plural = _("LMS Badges")


class LMSBadgeAssignment(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    badge = models.ForeignKey(LMSBatch, on_delete=models.CASCADE, verbose_name=_("Badge"))
    issued_on = models.DateField(verbose_name=_("Issued On"))
    badge_image = models.ImageField(upload_to='badge_images/', verbose_name=_("Badge Image"))
    badge_description = models.TextField(verbose_name=_("Badge Description"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))

    class Meta:
        verbose_name = _("LMS Badge Assignment")
        verbose_name_plural = _("LMS Badge Assignments")


class LMSCertificate(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    evaluator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='evaluator',
                                  verbose_name=_("Evaluator"))
    evaluator_name = models.CharField(max_length=255, verbose_name=_("Evaluator Name"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiry_date = models.DateField(verbose_name=_("Expiry Date"), null=True, blank=True)
    # template = models.ForeignKey('PrintFormat', on_delete=models.CASCADE, verbose_name=_("Template"))
    published = models.BooleanField(default=False, verbose_name=_("Publish on Participant Page"))
    course = RelatedCourseField(verbose_name=_("Course"))
    course_title = models.CharField(max_length=255, verbose_name=_("Course Title"))
    batch_name = models.ForeignKey(LMSBatch, on_delete=models.CASCADE, verbose_name=_("Batch"))
    batch_title = models.CharField(max_length=255, verbose_name=_("Batch Title"))

    class Meta:
        verbose_name = _("LMS Certificate")
        verbose_name_plural = _("LMS Certificates")


class LMSCertificateEvaluation(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    course = RelatedCourseField(verbose_name=_("Course"))
    batch_name = models.ForeignKey(LMSBatch, on_delete=models.CASCADE, verbose_name=_("Batch Name"))
    evaluator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='certificate_evaluator',
                                  verbose_name=_("Evaluator"))
    evaluator_name = models.CharField(max_length=255, verbose_name=_("Evaluator Name"))
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"), null=True, blank=True)
    rating = models.IntegerField(verbose_name=_("Rating"), null=True, blank=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, verbose_name=_("Status"))
    summary = models.TextField(verbose_name=_("Summary"), null=True, blank=True)

    class Meta:
        verbose_name = _("LMS Certificate Evaluation")
        verbose_name_plural = _("LMS Certificate Evaluations")


class LMSCertificateRequest(AbstractTimestampedModel):
    course = RelatedCourseField(verbose_name=_("Course"))
    course_title = models.CharField(max_length=255, verbose_name=_("Course Title"))
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    evaluator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='request_evaluator',
                                  verbose_name=_("Evaluator"))
    evaluator_name = models.CharField(max_length=255, verbose_name=_("Evaluator Name"))
    batch_name = models.ForeignKey(LMSBatch, on_delete=models.CASCADE, verbose_name=_("Batch Name"))
    batch_title = models.CharField(max_length=255, verbose_name=_("Batch Title"))
    timezone = models.CharField(max_length=255, verbose_name=_("Timezone"))
    date = models.DateField(verbose_name=_("Date"))
    day = models.CharField(max_length=50, choices=DayChoices.choices, verbose_name=_("Day"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"), null=True, blank=True)
    google_meet_link = models.CharField(max_length=255, verbose_name=_("Google Meet Link"))
    status = models.CharField(max_length=50, choices=StatusChoices.choices, verbose_name=_("Status"))

    class Meta:
        verbose_name = _("LMS Certificate Request")
        verbose_name_plural = _("LMS Certificate Requests")
