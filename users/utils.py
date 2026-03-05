from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, code, purpose):
    """
    Send OTP code via email.
    This is a placeholder function. Implement actual email sending here.
    """
    subject_map = {
        'registration': 'Verify your email',
        'password_reset': 'Reset your password'
    }
    
    message_map = {
        'registration': f'Your verification code is: {code}\n\nThis code will expire in 10 minutes.',
        'password_reset': f'Your password reset code is: {code}\n\nThis code will expire in 10 minutes.'
    }
    
    subject = subject_map.get(purpose, 'Your OTP code')
    message = message_map.get(purpose, f'Your verification code is: {code}')
    
    # send_mail(
    #     subject,
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [email],
    #     fail_silently=False,
    # )
