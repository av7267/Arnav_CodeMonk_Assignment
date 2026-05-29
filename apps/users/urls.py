from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView


urlpatterns = [
    # User registration endpoint
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # JWT login endpoint
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),

    # Refresh expired access tokens
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]