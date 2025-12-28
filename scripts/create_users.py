import os
import django
import secrets
import string

# Use the project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Scheduler.Scheduler.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def gen_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Assumed usernames/emails — change if you want different names
super_username = 'admin'
super_email = 'admin@example.com'
regular_username = 'testuser'
regular_email = 'testuser@example.com'

created = []

# Create superuser if not exists
if not User.objects.filter(username=super_username).exists():
    super_password = gen_password(14)
    User.objects.create_superuser(username=super_username, email=super_email, password=super_password)
    print(f"SUPERUSER_CREATED {super_username} {super_email} {super_password}")
    created.append(('superuser', super_username, super_email, super_password))
else:
    print(f"SUPERUSER_EXISTS {super_username}")

# Create regular user if not exists
if not User.objects.filter(username=regular_username).exists():
    regular_password = gen_password(12)
    User.objects.create_user(username=regular_username, email=regular_email, password=regular_password)
    print(f"USER_CREATED {regular_username} {regular_email} {regular_password}")
    created.append(('user', regular_username, regular_email, regular_password))
else:
    print(f"USER_EXISTS {regular_username}")

if not created:
    print('NO_CHANGES')
else:
    print('\nCreated accounts:')
    for kind, u, e, p in created:
        print(f" - {kind}: {u} ({e}) pwd: {p}")
