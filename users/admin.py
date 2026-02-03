from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    """
    model = User

    # Fields to display in the list view
    list_display = [
        'username',
        'full_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined'
    ]

    # Fields to filter by in the admin
    list_filter = [
        'is_staff',
        'is_active',
        'is_superuser',
        'date_joined',
        'last_login'
    ]

    # Fields to search by
    search_fields = [
        'username',
        'full_name',
        'email',
    ]

    # Fields to order by
    ordering = ['-date_joined']

    # Fieldsets for the add/edit form
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'full_name',
                'email',
                "avatar",
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'full_name',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            )
        }),
    )

    # Read-only fields
    readonly_fields = ['last_login', 'date_joined']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Add new fields to 'Personal info' section
        for section in fieldsets:
            if section[0] == _('Personal info'):
                fields = list(section[1]['fields'])
                if 'phone_number' not in fields:
                    fields.append('phone_number')
                if 'language' not in fields:
                    fields.append('language')
                if 'email_verified' not in fields:
                    fields.append('email_verified')
                section[1]['fields'] = tuple(fields)
        return fieldsets


from .models import OTPCode

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'purpose', 'is_used', 'created_at', 'expires_at')
    list_filter = ('purpose', 'is_used', 'created_at')
    search_fields = ('email', 'code')
    readonly_fields = ('created_at',)
