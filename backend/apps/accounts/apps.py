from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "apps.accounts"

    def ready(self) -> None:
        # noinspection PyUnresolvedReferences
        import apps.accounts.signals
        return super().ready()
