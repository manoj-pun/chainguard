from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(required=False,allow_blank=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate_first_name(self,value):
        return value.strip().capitalize()
    
    def validate_last_name(self,value):
        if value:
            return value.strip().capitalize()
        return value
        
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        #no need to check for the email exists as handled by model unique
        # if User.objects.filter(email=attrs['email']).exists():
        #     raise serializers.ValidationError({"email": "Email already registered."})
        attrs.pop('confirm_password')
        return attrs
    

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'avatar']