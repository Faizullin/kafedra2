from django.urls import path

from . import views

urlpatterns = [
    path("api/dash/content-editor/action/", views.ContentEditorActionAPIView.as_view(), name="content-editor-action-api"),
]
