from rest_framework import views
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer,UserDataSerializer
from . import services
from rest_framework.response import Response
from rest_framework import status
from .models import User

class RegisterUserAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        user = services.register_user(**serializer.validated_data)
        # or
        # user = services.register_user(
        #     first_name=serializer.validated_data["first_name"],
        #     last_name=serializer.validated_data.get("last_name",""),
        #     password=serializer.validated_data["password"],
        #     email=serializer.validated_data["email"]
        # )
        # or(without services)
        # user = User.objects.create_user(**serializer.validated_data)

        return Response(
            UserDataSerializer(user).data,
            status=status.HTTP_201_CREATED
        )