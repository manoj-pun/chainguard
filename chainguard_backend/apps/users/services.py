from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
import re
from django.db import transaction

"""Services for register"""
def register_user(*,first_name, last_name=None, email, password):
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name or "",
        password=password,
    )
    return user

"""Services for login"""
def login_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


"""Services for refresh token"""
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


"""Services for logout"""
def logout_user(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()


"""Services for assigning role with badge id"""
ROLE_PREFIX = {
    User.Role.OFFICER: "OFF",
    User.Role.STORAGE_CLERK: "SC",
    User.Role.ANALYST: "ANA",
}

def generate_badge_id(role):
    prefix = ROLE_PREFIX[role]
    last_user = (
        User.objects.filter(role=role)
        .exclude(badge_number__isnull=True)
        .order_by("-badge_number")
        .select_for_update()
        .first()
    )
    next_number = (last_user.badge_number + 1) if last_user else 1
    badge_id = f"{prefix}{next_number:03d}"
    return badge_id, next_number

@transaction.atomic
def assign_role(*, user, role):
    user = User.objects.select_for_update().get(id=user.id)

    if user.role != User.Role.PENDING:
        raise ValueError("User has already been assigned a role.")

    badge_id, badge_number = generate_badge_id(role)

    user.role = role
    user.badge_id = badge_id
    user.badge_number = badge_number
    user.save(update_fields=["role", "badge_id", "badge_number"])
    return user


"""Services for uploading the profile"""
def complete_profile(*, user, avatar):
    user.avatar = avatar
    user.profile_complete = True
    user.save(update_fields=["avatar", "profile_complete"])
    return user


"""Services for updating the user profile"""
def update_user(*, user, data):
    for field, value in data.items():
        setattr(user, field, value)
    user.save(update_fields=list(data.keys()))
    return user