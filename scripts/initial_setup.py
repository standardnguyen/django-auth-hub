"""
Script to create initial superuser and invite code.
Usage: python manage.py runscript initial_setup
"""
import os
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from authentication.models import InviteCode

User = get_user_model()

def run():
    """Create initial superuser and invite code if they don't exist"""
    
    # Create superuser if not exists
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
    
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save()
        print(f"Superuser created: {username} ({email})")
    else:
        user = User.objects.get(username=username)
        print(f"Superuser already exists: {username}")
    
    # Create initial invite code if none exist
    if not InviteCode.objects.exists():
        print("Creating initial invite code")
        code = InviteCode.generate_code()
        expires_at = timezone.now() + timedelta(days=7)
        
        InviteCode.objects.create(
            code=code,
            created_by=user,
            expires_at=expires_at
        )
        
        print(f"Created initial invite code: {code}")
        print(f"This invite code will expire on: {expires_at}")
    else:
        print("Invite codes already exist")
