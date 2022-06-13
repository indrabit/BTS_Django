from django.contrib import admin
from django.urls import path
from .views import Userlogin, create,ChangePasswordView,RequestPasswordResetEmailView,PasswordTokenCheckAPI

urlpatterns = [
    path('user/login/', Userlogin),
    # path('login/', Login.as_view(), name='login'),

    path('user/create/', create),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-reset-email/', RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name="password-reset-confirm")
]