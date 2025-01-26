from django.urls import path
from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsDashboardConfig
from lms.core.loading import get_class


class AttachmentsDashboardConfig(LmsDashboardConfig):
    label = "attachments_dashboard"
    name = "lms.apps.dashboard.attachments"
    verbose_name = _("Attachments")

    default_permissions = [
        "is_staff",
    ]

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "attachments-upload": (
                DashboardPermission.get("attachment"),
            ),
            "attachments-list": (
                DashboardPermission.get("attachment"),
            ),
            "attachments-action": (
                DashboardPermission.get("attachment"),
            ),
        }

    # pylint: disable=attribute-defined-outside-init
    def ready(self):
        self.attachments_list_api_view = get_class(
            "dashboard.attachments.api.views", "AttachmentListAPIView"
        )
        self.attachments_upload_api_view = get_class(
            "dashboard.attachments.api.views", "AttachmentUploadAPIView"
        )
        self.attachments_action_api_view = get_class(
            "dashboard.attachments.api.views", "AttachmentActionAPIView"
        )
        self.configure_permissions()

    def get_urls(self):
        urls = [
            path("api/v1/dashboard/attachments", self.attachments_list_api_view.as_view(), name="attachments-list-api"),
            path("api/v1/dashboard/attachments/upload", self.attachments_upload_api_view.as_view(), name="attachments-upload-api"),
            path("api/v1/dashboard/attachments/action", self.attachments_action_api_view.as_view(), name="attachments-action-api"),
        ]
        return self.post_process_urls(urls)
