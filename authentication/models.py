import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser for the auth hub.
    Additional fields and methods can be added as needed.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email is required
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


class InviteCode(models.Model):
    """
    Invite code model for managing user registrations.
    Only users with valid invite codes can register.
    """
    code = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_invites'
    )
    used_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='used_invite',
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('invite code')
        verbose_name_plural = _('invite codes')

    def __str__(self):
        return self.code

    @property
    def is_expired(self):
        """Check if invite code is expired"""
        return self.expires_at < timezone.now()

    @property
    def is_used(self):
        """Check if invite code has been used"""
        return self.used_by is not None

    @property
    def is_available(self):
        """Check if invite code is available for use"""
        return self.is_valid and not self.is_expired and not self.is_used
    
    @classmethod
    def generate_code(cls):
        """Generate a random invite code"""
        return str(uuid.uuid4()).replace('-', '')[:12].upper()


class TokenRecord(models.Model):
    """
    Model to track JWT tokens for potential invalidation.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='tokens'
    )
    jti = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('token record')
        verbose_name_plural = _('token records')
        
    def __str__(self):
        return f"{self.user.username}'s token ({self.jti})"
    
    @property
    def is_expired(self):
        """Check if token is expired"""
        return self.expires_at < timezone.now()
