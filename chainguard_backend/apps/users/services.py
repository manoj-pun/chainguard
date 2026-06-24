from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model

"""Register Services"""
def register_user(*,first_name, last_name=None, email, password):
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name or "",
        password=password,
    )
    return user

"""Login Services"""
def login_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


"""Refresh Token Services"""
def refresh_access_token(refresh_token):
    token = RefreshToken(refresh_token)

    result = {
        "access": str(token.access_token),
        "refresh": None,
    }

    if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS"):
        token.blacklist()

        user = get_user_model().objects.get(
            id=token["user_id"]
        )

        new_refresh = RefreshToken.for_user(user)
        result["refresh"] = str(new_refresh)

    return result


"""Logout Services"""
def logout_user(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()


"""Assign Role Services"""
def assign_role(*, user, role):
    user.role = role
    user.save(update_fields=['role'])
    return user


def complete_profile(*, user, avatar):
    user.avatar = avatar
    user.profile_complete = True
    user.save()
    return user


def update_user(*, user, data):
    for field, value in data.items():
        setattr(user, field, value)
    user.save(update_fields=list(data.keys()))
    return user