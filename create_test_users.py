from django.contrib.auth import get_user_model

User = get_user_model()

# Create test user
user, created = User.objects.get_or_create(
    username='testuser',
    email='test@minfin.uz',
    defaults={
        'full_name': 'Test User',
        'email_verified': True,
        'language': 'uz',
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print(f"✅ Created test user: {user.username} / test@minfin.uz / testpass123")
else:
    print(f"ℹ️  Test user already exists: {user.username}")

# Create admin user
admin, created = User.objects.get_or_create(
    username='admin',
    email='admin@minfin.uz',
    defaults={
        'full_name': 'Admin User',
        'is_staff': True,
        'is_superuser': True,
        'email_verified': True,
        'language': 'uz',
    }
)

if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✅ Created admin user: {admin.username} / admin@minfin.uz / admin123")
else:
    print(f"ℹ️  Admin user already exists: {admin.username}")
