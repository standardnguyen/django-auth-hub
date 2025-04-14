from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView,
    UserInfoView, UserListView, CreateInviteCodeView, ListInviteCodesView,
    InvalidateTokenView
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # User management endpoints
    path('users/me/', UserInfoView.as_view(), name='user_info'),
    path('users/', UserListView.as_view(), name='user_list'),
    
    # Invite code endpoints
    path('invites/create/', CreateInviteCodeView.as_view(), name='create_invite'),
    path('invites/list/', ListInviteCodesView.as_view(), name='list_invites'),
    
    # Token management endpoints
    path('tokens/invalidate/', InvalidateTokenView.as_view(), name='invalidate_token'),
]
