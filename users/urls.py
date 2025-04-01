from django.urls import path
from .views import (
    LoginView, 
    RegistrationView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]

