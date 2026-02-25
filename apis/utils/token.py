from datetime import datetime, timezone as dt_timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

def create_JWT_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh' : str(refresh),
        'access'  : str(refresh.access_token),
    }
    
    
class PasswordAwareJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        iat = validated_token.get("iat")
        if iat and user.password_changed_at:
            token_time = datetime.fromtimestamp(
                iat, tz=dt_timezone.utc
            )

            if token_time < user.password_changed_at:
                raise AuthenticationFailed(
                    "Password changed. Please login again."
                )

        return user