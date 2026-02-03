from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    full_name = models.CharField(
        _("Full Name"),
        max_length=255,
        blank=True,
        help_text=_("Enter your full name")
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=20,
        blank=True,
        help_text=_("Enter your phone number")
    )
    avatar = models.ImageField(
        _("Profile Avatar"),
        upload_to="user_avatars/",
        blank=True,
        null=True,
        help_text=_("Upload your profile avatar")
    )
    language = models.CharField(
        _("Language"),
        max_length=10,
        choices=[
            ('en', _('English')),
            ('uz', _('Uzbek')),
            ('ru', _('Russian')),
        ],
        default='uz',
        help_text=_("Preferred language")
    )
    email_verified = models.BooleanField(
        _("Email Verified"),
        default=False,
        help_text=_("Whether the email is verified")
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users_user"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.full_name or self.username

    def get_full_name(self):
        """Return the full name of the user."""
        return self.full_name or super().get_full_name()

    def get_short_name(self):
        """Return the short name of the user."""
        return self.full_name.split()[0] if self.full_name else self.username

    def get_avatar_url(self):
        """Return the URL of the user's avatar or None if not set."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None


class OTPCode(models.Model):
    """OTP code for email verification and password reset."""
    email = models.EmailField(
        _("Email"),
        help_text=_("Email address for OTP")
    )
    code = models.CharField(
        _("Code"),
        max_length=6,
        help_text=_("6-digit OTP code")
    )
    purpose = models.CharField(
        _("Purpose"),
        max_length=20,
        choices=[
            ('registration', _('Registration')),
            ('password_reset', _('Password Reset')),
        ],
        help_text=_("Purpose of the OTP")
    )
    is_used = models.BooleanField(
        _("Is Used"),
        default=False,
        help_text=_("Whether the OTP has been used")
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    expires_at = models.DateTimeField(
        _("Expires At"),
        help_text=_("Expiration time of the OTP")
    )

    class Meta:
        verbose_name = _("OTP Code")
        verbose_name_plural = _("OTP Codes")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['email', 'code', 'purpose']),
        ]

    def __str__(self):
        return f"{self.email} - {self.code} ({self.purpose})"

    @classmethod
    def create_otp(cls, email, purpose):
        """Create a new OTP code."""
        # Generate 6-digit code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Set expiration to 10 minutes from now
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Create and return the OTP
        otp = cls.objects.create(
            email=email,
            code=code,
            purpose=purpose,
            expires_at=expires_at
        )
        return otp

    def is_valid(self):
        """Check if the OTP is still valid (not expired and not used)."""
        return not self.is_used and timezone.now() < self.expires_at