from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with the custom User model'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')
        parser.add_argument('--full-name', type=str, help='Full name for the superuser')

    def handle(self, *args, **options):
        username = options['username'] or 'admin'
        email = options['email'] or 'admin@example.com'
        password = options['password'] or 'admin123'
        full_name = options['full_name'] or 'Administrator'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User with username "{username}" already exists.')
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name=full_name
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created superuser "{username}" with email "{email}"'
            )
        ) 