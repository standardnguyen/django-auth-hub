from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import InviteCode, TokenRecord, User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_admin', 'created_at')
        read_only_fields = ('id', 'is_admin', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with invite code"""
    
    invite_code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'invite_code')
    
    def validate(self, attrs):
        # Validate passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate invite code
        try:
            invite_code = InviteCode.objects.get(code=attrs['invite_code'])
            if not invite_code.is_available:
                if invite_code.is_used:
                    raise serializers.ValidationError({"invite_code": "This invite code has already been used."})
                elif invite_code.is_expired:
                    raise serializers.ValidationError({"invite_code": "This invite code has expired."})
                else:
                    raise serializers.ValidationError({"invite_code": "This invite code is not valid."})
        except InviteCode.DoesNotExist:
            raise serializers.ValidationError({"invite_code": "Invalid invite code."})
        
        return attrs
    
    def create(self, validated_data):
        # Get and remove invite code from validated data
        invite_code = InviteCode.objects.get(code=validated_data.pop('invite_code'))
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Mark invite code as used
        invite_code.used_by = user
        invite_code.used_at = timezone.now()
        invite_code.save()
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that records tokens in the database
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get tokens from the validated data
        refresh = self.get_token(self.user)
        
        # Record refresh token for potential invalidation
        TokenRecord.objects.create(
            user=self.user,
            jti=refresh['jti'],
            expires_at=timezone.now() + refresh.lifetime,
        )
        
        # Record access token for potential invalidation
        access_token = refresh.access_token
        TokenRecord.objects.create(
            user=self.user,
            jti=access_token['jti'],
            expires_at=timezone.now() + access_token.lifetime,
        )
        
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom token refresh serializer that records the new tokens
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get the refresh token from the request
        refresh = RefreshToken(attrs['refresh'])
        
        # Get the user from the token
        user_id = refresh.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Record new access token
        access_token = RefreshToken(attrs['refresh']).access_token
        TokenRecord.objects.create(
            user=user,
            jti=access_token['jti'],
            expires_at=timezone.now() + access_token.lifetime,
        )
        
        return data


class InviteCodeSerializer(serializers.ModelSerializer):
    """Serializer for invite codes"""
    
    created_by_username = serializers.SerializerMethodField()
    used_by_username = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = InviteCode
        fields = (
            'id', 'code', 'created_by', 'created_by_username', 
            'used_by', 'used_by_username', 'created_at', 
            'used_at', 'expires_at', 'is_valid', 'status'
        )
        read_only_fields = (
            'id', 'code', 'created_by', 'created_by_username',
            'used_by', 'used_by_username', 'created_at',
            'used_at', 'status'
        )
    
    def get_created_by_username(self, obj):
        return obj.created_by.username if obj.created_by else None
    
    def get_used_by_username(self, obj):
        return obj.used_by.username if obj.used_by else None
    
    def get_status(self, obj):
        if not obj.is_valid:
            return "Invalid"
        if obj.is_used:
            return "Used"
        if obj.is_expired:
            return "Expired"
        return "Available"
