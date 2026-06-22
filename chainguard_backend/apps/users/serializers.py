from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    """
        Serializer for handling user registration.
        Takes first_name,last_name,email,password,confirm_password as input
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs = {
            "first_name":{"max_length":30,"required":True},
            "last_name":{"max_length":30, "required":False,"allow_blank":True}
        }

    def validate_first_name(self,value):
        """Strip whitespace and capitalize the first letter of the first name."""
        return value.strip().capitalize()
    
    def validate_last_name(self,value):
        """Strip whitespace and capitalize the first letter of the last name if provided."""
        if value:
            return value.strip().capitalize()
        return value
        
    def validate(self, attrs):
        """Perform cross-field validation to ensure password matching."""
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        attrs.pop('confirm_password')
        return attrs
    


class UserDataSerializer(serializers.ModelSerializer):
    """Serializer for representing public user profile data."""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'avatar']