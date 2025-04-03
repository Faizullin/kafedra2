from django.utils.translation import gettext_lazy as _

from lms.core.compat import get_user_model
from utils.models import AbstractTimestampedModel, AbstractSlugModel, models

UserModel = get_user_model()


class RelatedCourseField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'LMSCourse'
        kwargs['on_delete'] = kwargs.get('on_delete', models.CASCADE)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _("Related Course"))
        super().__init__(*args, **kwargs)


class BatchCourse(AbstractTimestampedModel):
    course = RelatedCourseField()
    title = models.CharField(max_length=255, verbose_name=_("Course Title"))
    evaluator = models.ForeignKey('CourseEvaluator', on_delete=models.CASCADE, verbose_name=_("Evaluator"))

    class Meta:
        verbose_name = _("Batch Course")
        verbose_name_plural = _("Batch Courses")


class RelatedCohortField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'Cohort'
        kwargs['on_delete'] = kwargs.get('on_delete', models.CASCADE)
        kwargs['verbose_name'] = kwargs.get('verbose_name', _("Cohort"))
        super().__init__(*args, **kwargs)


class Cohort(AbstractTimestampedModel, AbstractSlugModel):
    course = RelatedCourseField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    instructor = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Instructor"))
    status = models.CharField(max_length=50,
                              choices=[('Upcoming', _('Upcoming')), ('Live', _('Live')), ('Completed', _('Completed')),
                                       ('Cancelled', _('Cancelled'))], verbose_name=_("Status"))
    begin_date = models.DateField(verbose_name=_("Begin Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    duration = models.CharField(max_length=255, verbose_name=_("Duration"))
    description = models.TextField(verbose_name=_("Description"))
    pages = models.ManyToManyField('CohortWebPage', verbose_name=_("Pages"))

    class Meta:
        verbose_name = _("Cohort")
        verbose_name_plural = _("Cohorts")


class CohortSubgroup(AbstractTimestampedModel, AbstractSlugModel):
    cohort = RelatedCohortField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    invite_code = models.CharField(max_length=255, verbose_name=_("Invite Code"))
    course = RelatedCourseField()

    class Meta:
        verbose_name = _("Cohort Subgroup")
        verbose_name_plural = _("Cohort Subgroups")


class CohortWebPage(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    template = models.ForeignKey('WebTemplate', on_delete=models.CASCADE, verbose_name=_("Template"))
    scope = models.CharField(max_length=50, choices=[('Cohort', _('Cohort')), ('Subgroup', _('Subgroup'))],
                             default='Cohort', verbose_name=_("Scope"))
    required_role = models.CharField(max_length=50, choices=[('Public', _('Public')), ('Student', _('Student')),
                                                             ('Mentor', _('Mentor')), ('Admin', _('Admin'))],
                                     default='Public', verbose_name=_("Required Role"))

    class Meta:
        verbose_name = _("Cohort Web Page")
        verbose_name_plural = _("Cohort Web Pages")


class CourseChapter(AbstractTimestampedModel):
    course = RelatedCourseField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    lessons = models.ManyToManyField('LessonReference', verbose_name=_("Lessons"))
    is_scorm_package = models.BooleanField(default=False, verbose_name=_("Is SCORM Package"))
    manifest_file = models.TextField(verbose_name=_("Manifest File"))
    launch_file = models.TextField(verbose_name=_("Launch File"))
    scorm_package = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name=_("SCORM Package"))
    scorm_package_path = models.TextField(verbose_name=_("SCORM Package Path"))
    course_title = models.CharField(max_length=255, verbose_name=_("Course Title"))

    class Meta:
        verbose_name = _("Course Chapter")
        verbose_name_plural = _("Course Chapters")


class CourseEvaluator(AbstractTimestampedModel):
    evaluator = models.ForeignKey(UserModel, on_delete=models.CASCADE, unique=True, verbose_name=_("Evaluator"))
    schedule = models.ManyToManyField('EvaluatorSchedule', verbose_name=_("Schedule"))
    unavailable_from = models.DateField(verbose_name=_("Unavailable From"))
    unavailable_to = models.DateField(verbose_name=_("Unavailable To"))

    class Meta:
        verbose_name = _("Course Evaluator")
        verbose_name_plural = _("Course Evaluators")


class CourseInstructor(AbstractTimestampedModel):
    instructor = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Instructor"))

    class Meta:
        verbose_name = _("Course Instructor")
        verbose_name_plural = _("Course Instructors")


class CourseLesson(AbstractTimestampedModel):
    chapter = models.ForeignKey('CourseChapter', on_delete=models.CASCADE, verbose_name=_("Course Chapter"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    body = models.TextField(verbose_name=_("Body"))
    youtube = models.CharField(max_length=255, verbose_name=_("YouTube Video URL"))
    question = models.TextField(verbose_name=_("Question"))
    file_type = models.CharField(max_length=50,
                                 choices=[('Image', _('Image')), ('Document', _('Document')), ('PDF', _('PDF'))],
                                 verbose_name=_("File Type"))
    instructor_notes = models.TextField(verbose_name=_("Instructor Notes"))
    content = models.TextField(verbose_name=_("Content"))
    instructor_content = models.TextField(verbose_name=_("Instructor Content"))
    is_scorm_package = models.BooleanField(default=False, verbose_name=_("Is SCORM Package"))
    course = RelatedCourseField()

    class Meta:
        verbose_name = _("Course Lesson")
        verbose_name_plural = _("Course Lessons")


class LMSProgram(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=255, unique=True, verbose_name=_("Title"))
    program_members = models.ManyToManyField('LMSProgramMember', verbose_name=_("Program Members"))

    class Meta:
        verbose_name = _("LMS Program")
        verbose_name_plural = _("LMS Programs")


class LMSCourse(AbstractTimestampedModel, AbstractSlugModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    published = models.BooleanField(default=False, verbose_name=_("Published"))
    video_link = models.CharField(max_length=255, verbose_name=_("Video Link"))
    short_introduction = models.TextField(verbose_name=_("Short Introduction"))
    disable_self_learning = models.BooleanField(default=False, verbose_name=_("Disable Self Learning"))
    image = models.ImageField(upload_to='course_images/', verbose_name=_("Image"))
    tags = models.CharField(max_length=255, verbose_name=_("Tags"))
    upcoming = models.BooleanField(default=False, verbose_name=_("Upcoming"))
    chapters = models.ManyToManyField('ChapterReference', verbose_name=_("Chapters"))
    instructors = models.ManyToManyField('CourseInstructor', verbose_name=_("Instructors"))
    enable_certification = models.BooleanField(default=False, verbose_name=_("Enable Certification"))
    related_courses = models.ManyToManyField('LMSCourse', verbose_name=_("Related Courses"))
    status = models.CharField(max_length=50,
                              choices=[('In Progress', _('In Progress')), ('Under Review', _('Under Review')),
                                       ('Approved', _('Approved'))], default='In Progress', verbose_name=_("Status"))
    # currency = models.ForeignKey('Currency', on_delete=models.CASCADE, verbose_name=_("Currency"))
    paid_course = models.BooleanField(default=False, verbose_name=_("Paid Course"))
    course_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Course Price"))
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount USD"))
    published_on = models.DateField(verbose_name=_("Published On"))
    featured = models.BooleanField(default=False, verbose_name=_("Featured"))
    enrollments = models.IntegerField(default=0, verbose_name=_("Enrollments"))
    lessons = models.IntegerField(default=0, verbose_name=_("Lessons"))
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_("Rating"))
    paid_certificate = models.BooleanField(default=False, verbose_name=_("Paid Certificate"))
    evaluator = models.ForeignKey(CourseEvaluator, on_delete=models.CASCADE, verbose_name=_("Evaluator"))

    program = models.ForeignKey(LMSProgram, on_delete=models.CASCADE, verbose_name=_("Program"),
                                related_name='courses', null=True, blank=True)

    class Meta:
        verbose_name = _("LMS Course")
        verbose_name_plural = _("LMS Courses")


class LMSCourseInterest(AbstractTimestampedModel):
    course = RelatedCourseField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("User"))
    email_sent = models.BooleanField(default=False, verbose_name=_("Email Sent"))

    class Meta:
        verbose_name = _("LMS Course Interest")
        verbose_name_plural = _("LMS Course Interests")


class LMSCourseMentorMapping(AbstractTimestampedModel):
    course = RelatedCourseField()
    mentor = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Mentor"))
    mentor_name = models.CharField(max_length=255, verbose_name=_("Mentor Name"))

    class Meta:
        verbose_name = _("LMS Course Mentor Mapping")
        verbose_name_plural = _("LMS Course Mentor Mappings")


class LMSCourseProgress(AbstractTimestampedModel):
    course = RelatedCourseField()
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, verbose_name=_("Chapter"))
    lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE, verbose_name=_("Lesson"))
    status = models.CharField(max_length=50,
                              choices=[('Complete', _('Complete')), ('Partially Complete', _('Partially Complete')),
                                       ('Incomplete', _('Incomplete'))], verbose_name=_("Status"))
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))

    class Meta:
        verbose_name = _("LMS Course Progress")
        verbose_name_plural = _("LMS Course Progresses")


class LMSCourseReview(AbstractTimestampedModel):
    review = models.TextField(verbose_name=_("Review"))
    rating = models.IntegerField(verbose_name=_("Rating"))
    course = RelatedCourseField()

    class Meta:
        verbose_name = _("LMS Course Review")
        verbose_name_plural = _("LMS Course Reviews")


class LMSBatch(AbstractTimestampedModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    description = models.TextField(verbose_name=_("Description"))
    courses = models.ManyToManyField('BatchCourse', verbose_name=_("Courses"))
    custom_component = models.TextField(verbose_name=_("Custom Component"))
    paid_batch = models.BooleanField(default=False, verbose_name=_("Paid Batch"))
    seat_count = models.IntegerField(verbose_name=_("Seat Count"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))
    assessment = models.ManyToManyField('LMSAssessment', verbose_name=_("Assessment"))
    medium = models.CharField(max_length=50, choices=[('Online', _('Online')), ('Offline', _('Offline'))],
                              default='Online', verbose_name=_("Medium"))
    category = models.ForeignKey('LMSCategory', on_delete=models.CASCADE, verbose_name=_("Category"))
    schedule = models.ManyToManyField('LMSTimetable', verbose_name=_("Schedule"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, verbose_name=_("Currency"))
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount USD"))
    published = models.BooleanField(default=False, verbose_name=_("Published"))
    instructors = models.ManyToManyField('CourseInstructor', verbose_name=_("Instructors"))
    confirmation_email_template = models.ForeignKey('EmailTemplate', on_delete=models.CASCADE,
                                                    verbose_name=_("Confirmation Email Template"))
    certification = models.BooleanField(default=False, verbose_name=_("Certification"))
    timezone = models.CharField(max_length=255, verbose_name=_("Timezone"))
    show_live_class = models.BooleanField(default=False, verbose_name=_("Show Live Class"))
    allow_future = models.BooleanField(default=True, verbose_name=_("Allow Future"))
    evaluation_end_date = models.DateField(verbose_name=_("Evaluation End Date"))
    meta_image = models.ImageField(upload_to='batch_images/', verbose_name=_("Meta Image"))
    custom_script = models.TextField(verbose_name=_("Custom Script"))

    class Meta:
        verbose_name = _("LMS Batch")
        verbose_name_plural = _("LMS Batches")


class LMSBatchEnrollment(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    member_username = models.CharField(max_length=255, verbose_name=_("Member Username"))
    batch = models.ForeignKey('LMSBatch', on_delete=models.CASCADE, verbose_name=_("Batch"))
    payment = models.ForeignKey('LMSPayment', on_delete=models.CASCADE, verbose_name=_("Payment"))
    source = models.ForeignKey('LMSSource', on_delete=models.CASCADE, verbose_name=_("Source"))
    confirmation_email_sent = models.BooleanField(default=False, verbose_name=_("Confirmation Email Sent"))

    class Meta:
        verbose_name = _("LMS Batch Enrollment")
        verbose_name_plural = _("LMS Batch Enrollments")


class LMSBatchFeedback(AbstractTimestampedModel):
    member = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Member"))
    batch = models.ForeignKey('LMSBatch', on_delete=models.CASCADE, verbose_name=_("Batch"))
    feedback = models.TextField(verbose_name=_("Feedback"))
    content = models.IntegerField(verbose_name=_("Content"))
    instructors = models.IntegerField(verbose_name=_("Instructors"))
    value = models.IntegerField(verbose_name=_("Value"))
    member_name = models.CharField(max_length=255, verbose_name=_("Member Name"))
    member_image = models.ImageField(upload_to='member_images/', verbose_name=_("Member Image"))

    class Meta:
        verbose_name = _("LMS Batch Feedback")
        verbose_name_plural = _("LMS Batch Feedbacks")

# class LMSBatchOld(AbstractTimestampedModel):
#     course = models.ForeignKey('LMSCourse', on_delete=models.CASCADE, verbose_name=_("Course"))
#     title = models.CharField(max_length=255, verbose_name=_("Title"))
#     description = models.TextField(verbose_name=_("Description"))
#     visibility = models.CharField(max_length=50, choices=[('Public', _('Public')), ('Unlisted', _('Unlisted')),
#                                                           ('Private', _('Private'))], default='Public',
#                                   verbose_name=_("Visibility"))
#     membership = models.CharField(max_length=50, choices=[('Open', _('Open')), ('Restricted', _('Restricted')),
#                                                           ('Invite Only', _('Invite Only')), ('Closed', _('Closed'))],
#                                   verbose_name=_("Membership"))
#     status = models.CharField(max_length=50, choices=[('Active', _('Active')), ('Inactive', _('Inactive'))],
#                               default='Active', verbose_name=_("Status"))
#     stage = models.CharField(max_length=50, choices=[('Ready', _('Ready')), ('In Progress', _('In Progress')),
#                                                      ('Completed', _('Completed')), ('Cancelled', _('Cancelled'))],
#                              default='Ready', verbose_name=_("Stage"))
#     start_date = models.DateField(verbose_name=_("Start Date"))
#     start_time = models.TimeField(verbose_name=_("Start Time"))
#     sessions_on = models.CharField(max_length=255, verbose_name=_("Sessions On"))
#     end_time = models.TimeField(verbose_name=_("End Time"))
#
#     class Meta:
#         verbose_name = _("LMS Batch Old")
#         verbose_name_plural = _("LMS Batch Olds")
#

# class LMSBatchTimetable(AbstractTimestampedModel):
#     reference_doctype = models.ForeignKey('DocType', on_delete=models.CASCADE, verbose_name=_("Reference DocType"))
#     reference_docname = models.CharField(max_length=255, verbose_name=_("Reference DocName"))
#     date = models.DateField(verbose_name=_("Date"))
#     start_time = models.TimeField(verbose_name=_("Start Time"))
#     end_time = models.TimeField(verbose_name=_("End Time"))
#     duration = models.CharField(max_length=255, verbose_name=_("Duration"))
#     milestone = models.BooleanField(default=False, verbose_name=_("Milestone"))
#
#     class Meta:
#         verbose_name = _("LMS Batch Timetable")
#         verbose_name_plural = _("LMS Batch Timetables")
