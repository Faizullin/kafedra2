from django.apps import apps
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsDashboardConfig
from lms.core.loading import get_class


class DashboardConfig(LmsDashboardConfig):
    label = "dashboard"
    name = "lms.apps.dashboard"
    verbose_name = _("Dashboard")

    namespace = "dashboard"

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "index": (
                DashboardPermission.staff,
                DashboardPermission.partner_dashboard_access,
            ),
        }

    def ready(self):
        self.index_view = get_class("dashboard.views", "IndexView")
        self.login_view = get_class("dashboard.views", "LoginView")

        self.resources_app = apps.get_app_config("resources_dashboard")
        self.attachments_app = apps.get_app_config("attachments_dashboard")
        self.share_access_app = apps.get_app_config("share_access_dashboard")
        self.configure_permissions()

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        print("dashboard.get_urls")
        print(self.share_access_app.urls)
        urls = [
            path("dashboard/", self.index_view.as_view(), name="index"),
            path("", include(self.share_access_app.urls[0])),
            path("", include(self.resources_app.urls[0])),
            path("", include(self.attachments_app.urls[0])),
            path("dashboard/login/", self.login_view.as_view(), name="login"),
            path(
                "dashboard/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
            ),
        ]
        return self.post_process_urls(urls)
