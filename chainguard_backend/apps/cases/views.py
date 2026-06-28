from .serializers import CaseCreateSerializer, CaseListSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .models import Case
from apps.common.permissions import IsOfficer, IsProfileComplete
from rest_framework.permissions import IsAuthenticated
from .services import create_case

class CaseCreateAPIView(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOfficer(),IsProfileComplete()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CaseCreateSerializer
        return CaseListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return Case.objects.all()
        if user.role == "OFFICER":
            return Case.objects.filter(officer=user)
        if user.role == "STORAGE_CLERK":
            return Case.objects.filter(status__in=[
                Case.Status.SUBMITTED_TO_STORAGE,
                Case.Status.IN_STORAGE,
                Case.Status.WITH_ANALYST,
                Case.Status.UNDER_REVIEW,
                Case.Status.SENT_TO_COURT,
            ])
        if user.role == "ANALYST":
            return Case.objects.filter(status=Case.Status.WITH_ANALYST)
        return Case.objects.none()
    
    def perform_create(self, serializer):
        case = create_case(
            officer = self.request.user,
            validated_data = serializer.validated_data
        )
        serializer.instance = case
    


