from django.apps import AppConfig


class AttachmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.attachments'
    
    def ready(self) -> None:
        # noinspection PyUnresolvedReferences
        import apps.attachments.signals
        return super().ready()