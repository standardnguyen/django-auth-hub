from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, InviteCode, TokenRecord
from .serializers import (
    UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer, InviteCodeSerializer
)


class RegisterView(generics.CreateAPIView):
    """API view for user registration with invite code"""
    
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view that uses our serializer"""
    
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view that uses our serializer"""
    
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    """API view for user logout (token invalidation)"""
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Get token from request
            token = RefreshToken(refresh_token)
            
            # Invalidate the refresh token
            jti = token.get('jti')
            token_record = TokenRecord.objects.get(jti=jti)
            token_record.is_valid = False
            token_record.save()
            
            # Invalidate any associated access tokens
            user_id = token.get('user_id')
            TokenRecord.objects.filter(
                user_id=user_id,
                expires_at__gt=timezone.now(),
                is_valid=True
            ).update(is_valid=False)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(generics.RetrieveAPIView):
    """API view for retrieving current user info"""
    
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """API view for listing all users (admin only)"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # Check if user is admin
        if not self.request.user.is_admin and not self.request.user.is_superuser:
            return User.objects.none()
        return User.objects.all()


class CreateInviteCodeView(APIView):
    """API view for creating a new invite code"""
    
    def post(self, request):
        # Check if user has permission to create invite codes
        if not request.user.is_admin and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to create invite codes"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create invite code
        expires_at = timezone.now() + timedelta(days=7)  # Default 7 days
        
        if 'expires_at' in request.data:
            try:
                days = int(request.data.get('expires_at'))
                expires_at = timezone.now() + timedelta(days=days)
            except (ValueError, TypeError):
                pass
        
        invite_code = InviteCode.objects.create(
            code=InviteCode.generate_code(),
            created_by=request.user,
            expires_at=expires_at
        )
        
        serializer = InviteCodeSerializer(invite_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListInviteCodesView(generics.ListAPIView):
    """API view for listing invite codes"""
    
    serializer_class = InviteCodeSerializer
    
    def get_queryset(self):
        # Admin can see all invite codes
        if self.request.user.is_admin or self.request.user.is_superuser:
            return InviteCode.objects.all().order_by('-created_at')
        
        # Regular users can only see their own invite codes
        return InviteCode.objects.filter(created_by=self.request.user).order_by('-created_at')


class InvalidateTokenView(APIView):
    """API view for invalidating a specific token (admin only)"""
    
    def post(self, request):
        # Check if user is admin
        if not request.user.is_admin and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to invalidate tokens"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get user and token from request
        user_id = request.data.get('user_id')
        token_id = request.data.get('token_id')
        
        if not user_id and not token_id:
            return Response(
                {"detail": "Either user_id or token_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Invalidate tokens
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                count = TokenRecord.objects.filter(
                    user=user,
                    expires_at__gt=timezone.now(),
                    is_valid=True
                ).update(is_valid=False)
                
                return Response({"detail": f"Invalidated {count} tokens for user {user.username}"},
                               status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if token_id:
            try:
                token_record = TokenRecord.objects.get(id=token_id)
                token_record.is_valid = False
                token_record.save()
                
                return Response({"detail": f"Token for {token_record.user.username} invalidated"},
                               status=status.HTTP_200_OK)
            except TokenRecord.DoesNotExist:
                return Response({"detail": "Token not found"}, status=status.HTTP_404_NOT_FOUND)
