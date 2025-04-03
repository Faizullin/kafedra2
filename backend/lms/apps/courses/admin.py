from django.contrib import admin

from utils.admin import BaseAdmin
from .models import (
    BatchCourse,
    Cohort,
    CohortSubgroup,
    CohortWebPage,
    CourseChapter,
    CourseEvaluator,
    CourseInstructor,
    CourseLesson,
    LMSCourse,
    LMSCourseInterest,
    LMSCourseMentorMapping,
    LMSCourseProgress,
    LMSCourseReview,
    LMSProgram,
    LMSBatch,
    LMSBatchEnrollment,
    LMSBatchFeedback,
)


@admin.register(BatchCourse)
class BatchCourseAdmin(BaseAdmin):
    pass


@admin.register(Cohort)
class CohortAdmin(BaseAdmin):
    pass


@admin.register(CohortSubgroup)
class CohortSubgroupAdmin(BaseAdmin):
    pass


@admin.register(CohortWebPage)
class CohortWebPageAdmin(BaseAdmin):
    pass


@admin.register(CourseChapter)
class CourseChapterAdmin(BaseAdmin):
    pass


@admin.register(CourseEvaluator)
class CourseEvaluatorAdmin(BaseAdmin):
    pass


@admin.register(CourseInstructor)
class CourseInstructorAdmin(BaseAdmin):
    pass


@admin.register(CourseLesson)
class CourseLessonAdmin(BaseAdmin):
    pass


@admin.register(LMSCourse)
class LMSCourseAdmin(BaseAdmin):
    pass


@admin.register(LMSCourseInterest)
class LMSCourseInterestAdmin(BaseAdmin):
    pass


@admin.register(LMSCourseMentorMapping)
class LMSCourseMentorMappingAdmin(BaseAdmin):
    pass


@admin.register(LMSCourseProgress)
class LMSCourseProgressAdmin(BaseAdmin):
    pass


@admin.register(LMSCourseReview)
class LMSCourseReviewAdmin(BaseAdmin):
    pass


@admin.register(LMSProgram)
class LMSProgramAdmin(BaseAdmin):
    pass


@admin.register(LMSBatch)
class LMSBatchAdmin(BaseAdmin):
    pass


@admin.register(LMSBatchEnrollment)
class LMSBatchEnrollmentAdmin(BaseAdmin):
    pass


@admin.register(LMSBatchFeedback)
class LMSBatchFeedbackAdmin(BaseAdmin):
    pass
