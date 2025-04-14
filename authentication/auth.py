from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from .models import TokenRecord


class JWTAuthentication(BaseJWTAuthentication):
    """
    Custom JWT authentication that checks if token has been invalidated.
    Extends the SimpleJWT authentication to add token invalidation capability.
    """
    
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        Additionally checks if the token has been invalidated in the database.
        """
        # First get the user using the parent method
        user = super().get_user(validated_token)
        
        # Now check if the token has been invalidated
        jti = validated_token.get(api_settings.JTI_CLAIM)
        if jti:
            try:
                token_record = TokenRecord.objects.get(jti=jti)
                if not token_record.is_valid:
                    raise AuthenticationFailed(
                        'Token has been invalidated.',
                        code='token_invalidated',
                    )
            except TokenRecord.DoesNotExist:
                # If the token doesn't exist in our records, it's suspicious
                raise InvalidToken('Token is not recognized')
        
        return user
