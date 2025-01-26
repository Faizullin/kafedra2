from django.urls import path
from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsDashboardConfig
from lms.core.loading import get_class


class ResourcesDashboardConfig(LmsDashboardConfig):
    label = "resources_dashboard"
    name = "lms.apps.dashboard.resources"
    verbose_name = _("Resources")

    default_permissions = [
        "is_staff",
    ]

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "resources-post": (
                DashboardPermission.get("post"),
            ),
            "resources-post-create": (
                DashboardPermission.get("post"),
            ),
            "resources-post-list": (
                DashboardPermission.get("post"),
            ),
            "resources-post-delete": (
                DashboardPermission.get("post"),
            ),
        }

    # pylint: disable=attribute-defined-outside-init
    def ready(self):
        self.resources_post_list_view = get_class(
            "dashboard.resources.views", "ResourcesPostListView"
        )
        self.resources_post_list_api_view = get_class(
            "dashboard.resources.api.views", "ResourcesPostListAPIView"
        )
        self.resources_post_create_view = get_class(
            "dashboard.resources.views", "ResourcesPostCreateView"
        )
        self.resources_post_update_view = get_class(
            "dashboard.resources.views", "ResourcesPostUpdateView"
        )
        self.resources_post_edit_content_view = get_class(
            "dashboard.resources.views", "ResourcesPostEditContentView"
        )
        self.resources_post_edit_content_action_api_view = get_class(
            "dashboard.resources.api.views", "ResourcesPostEditContentActionAPIView"
        )
        self.resources_post_delete_view = get_class(
            "dashboard.resources.views", "ResourcesPostDeleteView"
        )
        self.configure_permissions()

    def get_urls(self):
        urls = [
            path("dashboard/resources/posts", self.resources_post_list_view.as_view(), name="resources-post-list"),
            path("api/v1/dashboard/resources/posts", self.resources_post_list_api_view.as_view(),
                 name="resources-post-list-api"),
            path(
                "dashboard/resources/posts/add",
                self.resources_post_create_view.as_view(),
                name="resources-post-create",
            ),
            path(
                "dashboard/resources/posts/<int:pk>/edit",
                self.resources_post_update_view.as_view(),
                name="resources-post-update",
            ),
            path(
                "dashboard/resources/posts/<int:pk>/edit-content",
                self.resources_post_edit_content_view.as_view(),
                name="resources-post-edit-content",
            ),
            path("api/v1/dashboard/resources/posts/edit-content/action",
                 self.resources_post_edit_content_action_api_view.as_view(),
                 name="resources-post-edit-content-action-api"),
            path(
                "dashboard/resources/posts/<int:pk>",
                self.resources_post_delete_view.as_view(),
                name="resources-post-delete",
            ),
        ]
        return self.post_process_urls(urls)
