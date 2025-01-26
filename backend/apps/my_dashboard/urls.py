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
    path(f"{dashboard_prefix}/courses/courses/", views.CourseListView.as_view(), name="courses-list"),
    path(f"{dashboard_prefix}/courses/courses/add/", views.CourseCreateView.as_view(), name="courses-add"),
    path(f"{dashboard_prefix}/courses/courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="courses-edit"),
    path(f"{dashboard_prefix}/courses/programs/", views.ProgramListView.as_view(), name="programs-list"),
    path(f"{dashboard_prefix}/courses/programs/add/", views.ProgramCreateView.as_view(), name="programs-add"),
    path(f"{dashboard_prefix}/courses/programs/<int:pk>/edit/", views.PostUpdateView.as_view(), name="programs-edit"),
    path(f"{dashboard_prefix}/courses/students/", views.StudentListView.as_view(), name="students-list"),

    path(f"{dashboard_prefix}/assignments/assignments", views.AssignmentListView.as_view(), name="assignments-assignments-list"),
    path(f"{dashboard_prefix}/assignments/assignments/add", views.AssignmentCreateView.as_view(), name="assignments-assignments-add"),
    path(f"{dashboard_prefix}/assignments/assignments/<int:pk>/edit/", views.AssignmentUpdateView.as_view(),  name="assignments-assignments-edit"),

    path(f"{dashboard_prefix}/assignments/quizzes", views.AssignmentListView.as_view(), name="assignments-quizzes-list"),
    path(f"{dashboard_prefix}/assignments/quizzes/add", views.AssignmentCreateView.as_view(), name="assignments-quizzes-add"),
    path(f"{dashboard_prefix}/assignments/quizzes/<int:pk>/edit/", views.AssignmentUpdateView.as_view(),  name="assignments-quizzes-edit"),


    path(f"{dashboard_prefix}/logs/activities/", views.ActivityLogListView.as_view(), name="activities-list"),

    # path("my_dashboard/", dashboard_view, name="my_dashboard"),
]
