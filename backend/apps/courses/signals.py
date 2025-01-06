from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.activities.models import ActivityLog
from apps.courses.models import Program


@receiver(post_save, sender=Program)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=_(f"The program '{instance}' has been {verb}."))


@receiver(post_delete, sender=Program)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=_(f"The program '{instance}' has been deleted."))