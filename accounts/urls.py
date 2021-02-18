from django.urls import path
from .api import RegisterAPI, LoginAPI, UserAPI, VerifyEmailAPI, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view(), name="register"),
    path('api/auth/email-verify', VerifyEmailAPI.as_view(), name="email-verify"),
    path('api/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/logout/', LogoutAPIView.as_view(), name="logout"),
    path('api/auth/user', UserAPI.as_view()),
]