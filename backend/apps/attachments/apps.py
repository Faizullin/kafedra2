from django.apps import AppConfig


class AttachmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.attachments'
    
    def ready(self) -> None:
        import apps.attachments.signals