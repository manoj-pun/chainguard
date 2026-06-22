from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer,UserDataSerializer
from . import services
from rest_framework.response import Response
from rest_framework import status

class RegisterUserAPIView(CreateAPIView):
    """API end point for user registration"""
    
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