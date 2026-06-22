from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

def register_user(*,first_name, last_name=None, email, password):
    """Create and return a new user instance using validated input data."""
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name or "",
        password=password,
    )
    return user


def login_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
