from django.urls import path

from .views import (PostListApiView, PostDetailApiView)

app_name = 'posts'

urlpatterns = [
    path('api/v1/posts/', PostListApiView.as_view(), name='post-list-api'),
    path('api/v1/posts/<slug:slug>/', PostDetailApiView.as_view(), name='post-retrieve-api'),
    # path('api/v1/site-document/<int:pk>/', SiteDocumentDetailApiView.as_view(), name='site-document-retrieve-api'),
    path(
        'image_upload/',
        staff_member_required(ImageUploadView.as_view()),
        name='editorjs_image_upload',
    ),
    # path(
    #     'linktool/',
    #     staff_member_required(LinkToolView.as_view()),
    #     name='editorjs_linktool',
    # ),
    # path(
    #     'image_by_url/',
    #     ImageByUrl.as_view(),
    #     name='editorjs_image_by_url',
    # ),

]
