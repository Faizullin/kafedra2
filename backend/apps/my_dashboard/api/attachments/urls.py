from django.urls import path

from . import views

urlpatterns = [
    path("api/dash/attachments/", views.AttachmentListAPIView.as_view(), name="attachments-list-api"),
    path("api/dash/attachments/upload/", views.AttachmentUploadAPIView.as_view(),
         name="attachments-upload-api"),
    path("api/dash/attachments/delete/", views.AttachmentDeleteAPIView.as_view(),
         name="attachments-delete-api"),
    path("api/dash/attachments/action/", views.AttachmentActionAPIView.as_view(),
         name="attachments-action-api"),
]
