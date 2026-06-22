from .models import User

def register_user(*,first_name, last_name=None, email, password):
    """Create and return a new user instance using validated input data."""
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name or "",
        password=password,
    )
    return user