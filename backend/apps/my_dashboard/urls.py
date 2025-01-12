from django.urls import path

from . import views
from .config import dashboard_prefix

app_name = "my_dashboard"

urlpatterns = [
    # Accounts url
    path(f"{dashboard_prefix}/", views.dashboard_home_view, name="home"),
    path(f"{dashboard_prefix}/resources/posts/", views.PostListView.as_view(), name="resources-posts-list"),
    path(f"{dashboard_prefix}/resources/posts/add/", views.PostCreateView.as_view(), name="posts-add"),
    path(f"{dashboard_prefix}/resources/posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="posts-edit"),
    path(f"{dashboard_prefix}/resources/posts/<int:pk>/edit/content/", views.PostEditContentView.as_view(), name="posts-edit-content"),
    path(f"{dashboard_prefix}/courses/", views.CourseListView.as_view(), name="courses-list"),
    path(f"{dashboard_prefix}/courses/add/", views.CourseCreateView.as_view(), name="courses-add"),
    path(f"{dashboard_prefix}/courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="courses-edit"),
    path(f"{dashboard_prefix}/programs/", views.ProgramListView.as_view(), name="programs-list"),
    path(f"{dashboard_prefix}/programs/add/", views.ProgramCreateView.as_view(), name="programs-add"),
    path(f"{dashboard_prefix}/programs/<int:pk>/edit/", views.PostUpdateView.as_view(), name="programs-edit"),
    path(f"{dashboard_prefix}/students/", views.StudentListView.as_view(), name="students-list"),
    path(f"{dashboard_prefix}/activities/", views.ActivityLogListView.as_view(), name="activities-list"),

    # path("my_dashboard/", dashboard_view, name="my_dashboard"),
]
