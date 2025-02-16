from django.apps import apps
from django.urls import include, path

from lms.apps.dashboard.apps import DashboardConfig as MyDashboardConfig


class DashboardConfig(MyDashboardConfig):
    name = "apps.dashboard"

    def ready(self):
        self.quiz_app = apps.get_app_config("quiz_dashboard")
        super().ready()

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        urls = [
            path("dashboard/", self.index_view.as_view(), name="index"),
            path("", include(self.resources_app.urls[0])),
            path("", include(self.attachments_app.urls[0])),
            path("", include(self.quiz_app.urls[0])),
            path("", include(self.share_access_app.urls[0])),
            path("dashboard/login/", self.login_view.as_view(), name="login"),
            path(
                "dashboard/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
            ),
        ]
        return self.post_process_urls(urls)
