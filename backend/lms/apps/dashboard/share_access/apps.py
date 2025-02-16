from django.urls import path
from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsDashboardConfig
from lms.core.loading import get_class


class ShareAccessDashboardConfig(LmsDashboardConfig):
    label = "share_access_dashboard"
    name = "lms.apps.dashboard.share_access"
    verbose_name = _("Share Access")

    namespace = "share_access"

    default_permissions = [
        "is_staff",
    ]


    def configure_permissions(self):
        pass
        # DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")
        #
        # self.permissions_map = {
        #     "resources-post": (
        #         DashboardPermission.get("post"),
        #     ),
        #     "resources-post-create": (
        #         DashboardPermission.get("post"),
        #     ),
        #     "resources-post-list": (
        #         DashboardPermission.get("post"),
        #     ),
        #     "resources-post-delete": (
        #         DashboardPermission.get("post"),
        #     ),
        # }


    def ready(self):
        self.share_access_obj_users_list_api_view = get_class("dashboard.share_access.api.views",
                                                              "ShareAccessObjUsersListAPIView")
        self.share_access_obj_users_update_api_view = get_class("dashboard.share_access.api.views",
                                                                "ShareAccessObjUsersUpdateAPIView")
        self.configure_permissions()

    def get_urls(self):
        urls = [
            path("api/v1/dashboard/share-access/obj-users/get-users", self.share_access_obj_users_list_api_view.as_view(),
                 name="share-access-obj-users-list-api"),
            path("api/v1/dashboard/share-access/obj-users/update", self.share_access_obj_users_update_api_view.as_view(),
                 name="share-access-obj-users-update-api"),
        ]
        return self.post_process_urls(urls)
