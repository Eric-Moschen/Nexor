from django.urls import path

from apps.accounts.views import ChangePasswordAPIView, LoginAPIView, LogoutAPIView, MeAPIView, RefreshAPIView

app_name = "auth"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshAPIView.as_view(), name="refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
]
