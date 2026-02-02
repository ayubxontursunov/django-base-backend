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
    readonly_fields = ['last_login', 'date_joined',]
