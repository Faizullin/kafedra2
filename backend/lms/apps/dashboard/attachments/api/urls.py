from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/dashboard/attachments/", views.AttachmentListAPIView.as_view(), name="attachments-list-api"),
    path("api/v1/dash/attachments/upload/", views.AttachmentUploadAPIView.as_view(),
         name="attachments-upload-api"),
    path("api/v1/dash/attachments/action/", views.AttachmentActionAPIView.as_view(),
         name="attachments-action-api"),
]
