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
    avatar = models.ImageField(
        _("Profile Avatar"),
        upload_to="user_avatars/",
        blank=True,
        null=True,
        help_text=_("Upload your profile avatar")
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