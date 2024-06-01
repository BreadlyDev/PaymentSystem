from django.urls import path
from . import views as v
from djoser.views import UserViewSet

# from djoser.views import (
#     PasswordResetView,
#     PasswordResetConfirmView
# )

urlpatterns = [
    path('password/reset/', UserViewSet.as_view({'post': 'reset_password'}), name='password-reset'),
    path('password/reset/confirm/', UserViewSet.as_view({'post': 'reset_password_confirm'}), name='password-reset-confirm'),

    path('register', v.RegisterAPIView.as_view()),
    path('login', v.LoginAPIView.as_view()),
    path('logout', v.LogoutAPIView.as_view()),
]
