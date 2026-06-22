from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.contrib.auth import authenticate

"""Serializer for handling user registration."""
class RegisterUserSerializer(serializers.ModelSerializer):
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
        return value.strip().capitalize()
    
    def validate_last_name(self,value):
        if value:
            return value.strip().capitalize()
        return value
        
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        attrs.pop('confirm_password')
        return attrs
    

"""Serializer for representing public user profile data."""
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'avatar']


"""Serializer for loggin in user"""
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        
        attrs["user"] = user
        return attrs
