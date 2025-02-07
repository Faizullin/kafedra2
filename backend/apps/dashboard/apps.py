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
            # path("catalogue/", include(self.catalogue_app.urls[0])),
            # path("reports/", include(self.reports_app.urls[0])),
            # path("orders/", include(self.orders_app.urls[0])),
            # path("users/", include(self.users_app.urls[0])),
            # path("pages/", include(self.pages_app.urls[0])),
            # path("partners/", include(self.partners_app.urls[0])),
            # path("offers/", include(self.offers_app.urls[0])),
            # path("ranges/", include(self.ranges_app.urls[0])),
            # path("reviews/", include(self.reviews_app.urls[0])),
            # path("vouchers/", include(self.vouchers_app.urls[0])),
            # path("comms/", include(self.comms_app.urls[0])),
            # path("shipping/", include(self.shipping_app.urls[0])),
            path("dashboard/login/", self.login_view.as_view(), name="login"),
            path(
                "dashboard/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
            ),
        ]
        return self.post_process_urls(urls)
