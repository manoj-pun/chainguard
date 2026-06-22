from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer,UserDataSerializer, LoginUserSerializer
from . import services
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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