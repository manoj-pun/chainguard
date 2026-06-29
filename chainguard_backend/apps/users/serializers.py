from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

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
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'avatar', 'badge_id']


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
    

"""Serializer for assigning the role"""
class AssignRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(User.Role.choices)


"""Serializer for uploading the profile"""
class CompleteProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField(use_url=True)


"""Serializer for updating the profile"""
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'avatar': {'required': False},
        }

    def validate_email(self, value):
        user = self.context.get('user')
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already in use.")
        return value