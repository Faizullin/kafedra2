from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .utils import (
#     generate_student_credentials,
#     generate_lecturer_credentials,
#     send_new_account_email,
# )

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def post_save_account_receiver(sender, instance: UserModel =None, created=False, *args, **kwargs):
    """
    Send email notification
    """
    if created:
        pass
        # if instance.is_student:
        #     username, password = generate_student_credentials()
        #     instance.username = username
        #     instance.set_password(password)
        #     instance.save()
        #     # Send email with the generated credentials
        #     send_new_account_email(instance, password)
        #
        # if instance.is_lecturer:
        #     username, password = generate_lecturer_credentials()
        #     instance.username = username
        #     instance.set_password(password)
        #     instance.save()
        #     # Send email with the generated credentials
        #     send_new_account_email(instance, password)
