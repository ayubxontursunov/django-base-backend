from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CheckEmailView, RegisterView, LoginView, ProfileView,
    VerifyOTPView, ResendOTPView, PasswordResetRequestView,
    PasswordResetConfirmView, PasswordChangeView
)

app_name = 'users'

urlpatterns = [
    # Email check
    path('check-email/', CheckEmailView.as_view(), name='check_email'),
    
    # Registration & OTP
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    
    # Login
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password Reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Profile
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
]
