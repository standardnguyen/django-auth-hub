from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, InviteCode, TokenRecord

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for the custom User model"""
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    """Admin configuration for InviteCode model"""
    list_display = ('code', 'created_by', 'used_by', 'created_at', 'used_at', 'expires_at', 'is_valid', 'is_available')
    list_filter = ('is_valid', 'created_at', 'expires_at')
    search_fields = ('code', 'created_by__username', 'used_by__username')
    readonly_fields = ('code', 'created_at', 'used_at')
    fieldsets = (
        (None, {'fields': ('code', 'created_by', 'used_by')}),
        (_('Status'), {'fields': ('is_valid',)}),
        (_('Dates'), {'fields': ('created_at', 'used_at', 'expires_at')}),
    )
    
    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True
    is_available.short_description = 'Available'


@admin.register(TokenRecord)
class TokenRecordAdmin(admin.ModelAdmin):
    """Admin configuration for TokenRecord model"""
    list_display = ('user', 'jti', 'created_at', 'expires_at', 'is_valid', 'is_expired')
    list_filter = ('is_valid', 'created_at', 'expires_at')
    search_fields = ('user__username', 'jti')
    readonly_fields = ('user', 'jti', 'created_at', 'expires_at')
    fieldsets = (
        (None, {'fields': ('user', 'jti')}),
        (_('Status'), {'fields': ('is_valid',)}),
        (_('Dates'), {'fields': ('created_at', 'expires_at')}),
    )
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'