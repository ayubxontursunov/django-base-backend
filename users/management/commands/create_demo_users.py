from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users (admin + test user) for local development"

    def add_arguments(self, parser):
        parser.add_argument("--admin-email", type=str, default="admin@example.com")
        parser.add_argument("--admin-password", type=str, default="admin123")
        parser.add_argument("--user-email", type=str, default="test@example.com")
        parser.add_argument("--user-password", type=str, default="testpass123")

    def handle(self, *args, **options):
        admin_email = options["admin_email"]
        admin_password = options["admin_password"]
        user_email = options["user_email"]
        user_password = options["user_password"]

        admin_username = admin_email.split("@")[0]
        user_username = user_email.split("@")[0]

        admin, admin_created = User.objects.get_or_create(
            username=admin_username,
            defaults={
                "email": admin_email,
                "full_name": "Admin User",
                "is_staff": True,
                "is_superuser": True,
                "email_verified": True,
            },
        )
        if admin_created:
            admin.set_password(admin_password)
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin "{admin_username}" ({admin_email})'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin "{admin_username}" already exists'))

        user, user_created = User.objects.get_or_create(
            username=user_username,
            defaults={
                "email": user_email,
                "full_name": "Test User",
                "email_verified": True,
            },
        )
        if user_created:
            user.set_password(user_password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user "{user_username}" ({user_email})'))
        else:
            self.stdout.write(self.style.WARNING(f'User "{user_username}" already exists'))

