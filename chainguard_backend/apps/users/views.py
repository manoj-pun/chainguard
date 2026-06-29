from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RegisterUserSerializer,
    UserDataSerializer, 
    LoginUserSerializer, 
    AssignRoleSerializer,
    CompleteProfileSerializer,
    UpdateUserSerializer
)
from . import services
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from apps.common.permissions import IsSupervisor
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

"""API end point for user registration"""
class RegisterUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.register_user(**serializer.validated_data)

        return Response(
            UserDataSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    

"""API end point for loging in user"""
class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        tokens = services.login_user(user)

        response = Response({
            "user": UserDataSerializer(user).data,
            "access": tokens["access"],   # access token in response body
        }, status=status.HTTP_200_OK)

        # refresh token in httpOnly cookie
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,      
            secure=True,        
            samesite='Lax',     
            max_age=7 * 24 * 60 * 60,  
        )

        return response
    

"""API end point to refresh token"""
class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            tokens = services.refresh_access_token(refresh_token)

            response = Response(
                {"access": tokens["access"]},
                status=status.HTTP_200_OK,
            )

            if tokens["refresh"]:
                response.set_cookie(
                    key="refresh_token",
                    value=tokens["refresh"],
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=7 * 24 * 60 * 60,
                )

            return response

        except TokenError:
            return Response(
                {"error": "Refresh token is invalid or expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    

"""API end point for loging out user"""
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            services.logout_user(refresh_token)
        except TokenError:
            return Response(
                {"error": "Token is invalid or already blacklisted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("refresh_token")
        return response
    

"""API end point for listing all users
    Only supervisor can list all users
"""
class UserListAPIView(ListAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = UserDataSerializer

    def get_queryset(self):
        return User.objects.exclude(role=User.Role.SUPERVISOR).order_by('role')
    

"""API end point for retrieving single user with id"""
class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = UserDataSerializer

    def get_queryset(self):
        return User.objects.exclude(role=User.Role.SUPERVISOR)
    

"""API end point for assigning roles"""
class AssignRoleAPIView(APIView):
    permission_classes = [IsSupervisor]

    def patch(self, request, pk):
        target_user = get_object_or_404(User, id=pk)
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = services.assign_role(
                user=target_user,
                role=serializer.validated_data['role']
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserDataSerializer(user).data, status=status.HTTP_200_OK)
    

"""API end point for uploading profile"""
class CompleteProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        if request.user.profile_complete:
            return Response(
                {"error": "Profile already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CompleteProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.complete_profile(
            user=request.user,
            avatar=serializer.validated_data['avatar']
        )

        return Response(UserDataSerializer(user,context={'request': request}).data, status=status.HTTP_200_OK)
    

"""API end point for updating profile"""
class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdateUserSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)

        user = services.update_user(
            user=request.user,
            data=serializer.validated_data
        )

        return Response(UserDataSerializer(user).data, status=status.HTTP_200_OK)