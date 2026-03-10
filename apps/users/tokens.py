# accounts/tokens.py
from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        # Get the standard token payload
        token = super().for_user(user)

        # Add custom claims here
        token['is_active'] = user.is_active
        # You could also add things like token['phone'] = user.phone if needed
        
        return token