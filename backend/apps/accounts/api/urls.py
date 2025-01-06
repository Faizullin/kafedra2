from django.urls import path
from . import views

app_name = "accounts_-api"

urlpatterns = [
    path("", views.UserListAPIView.as_view(), name="users-api"),
]
