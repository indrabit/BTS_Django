from django.contrib import admin
from django.urls import path
from .views import Userlogin, create,RequestPasswordResetEmailView,PasswordTokenCheckAPI,PasswordAPIView

urlpatterns = [
    path('user/login/',Userlogin),
    path('user/create/',create),
    path('request-reset-email/', RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name="password-reset-confirm"),
    path("passwordupdate/", PasswordAPIView.as_view(), name="password-detail")    
]