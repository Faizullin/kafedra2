from django.db.models.signals import pre_save
from django.dispatch import receiver

from lms.apps.courses.utils import unique_slug_generator
from lms.core.loading import get_model

Course = get_model("courses", "Course")


# @receiver(post_save, sender=Program)
# def log_save(sender, instance, created, **kwargs):
#     verb = "created" if created else "updated"
#     ActivityLog.objects.create(message=_(f"The program '{instance}' has been {verb}."))
#
#
# @receiver(post_delete, sender=Program)
# def log_delete(sender, instance, **kwargs):
#     ActivityLog.objects.create(message=_(f"The program '{instance}' has been deleted."))
#

@receiver(pre_save, sender=Course)
def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# @receiver(post_save, sender=Course)
# def log_save(sender, instance, created, **kwargs):
#     verb = "created" if created else "updated"
#     ActivityLog.objects.create(message=_(f"The course '{instance}' has been {verb}."))
#
#
# @receiver(post_delete, sender=Course)
# def log_delete(sender, instance, **kwargs):
#     ActivityLog.objects.create(message=_(f"The course '{instance}' has been deleted."))
