from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    LoginView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
)

urlpatterns = [

    # ==========================================
    # AUTHENTICATION
    # ==========================================

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]