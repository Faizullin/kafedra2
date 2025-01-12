from django.urls import path

from . import views
from .attachments.urls import urlpatterns as attachments_urls
from .content_editor.urls import urlpatterns as content_editor_urls

app_name = 'my_dashboard-api'

urlpatterns = [
                  path("api/dash/posts/", views.PostListAPIView.as_view(), name="posts-list-api"),
              ] + attachments_urls + content_editor_urls
