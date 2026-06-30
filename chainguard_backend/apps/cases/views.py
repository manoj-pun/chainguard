from .serializers import (
    CaseCreateSerializer, 
    CaseListSerializer,
    CaseDetailSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .models import Case
from apps.common.permissions import IsOfficer, IsProfileComplete, IsStorageClerk, IsAnlyst
from rest_framework.permissions import IsAuthenticated
from .services import create_case, submit_case_to_storage, acknowledge_case, submit_case_to_analyst
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

"""Create and list cases
    Create can only be done by officer
    List can only be done supervisor and officer can only list his cases
"""
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

    def create(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        case = create_case(
            officer = self.request.user,
            validated_data = serializer.validated_data
        )
        return Response(CaseListSerializer(case).data, status=status.HTTP_201_CREATED)

    
class CaseDetailAPIView(RetrieveAPIView):
    serializer_class = CaseDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return Case.objects.all()
        return Case.objects.filter(officer = user)


class SubmitCaseToStorageAPIView(APIView):
    permission_classes = [IsOfficer, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk, officer=request.user)

        try:
            submit_case_to_storage(case=case, officer=request.user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Case submitted to storage."}, status=status.HTTP_200_OK)
    

class AcknowledgeCaseAPIView(APIView):
    permission_classes = [IsStorageClerk, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            acknowledge_case(case=case, storage_clerk=request.user)
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case Acknowledged"}, status=status.HTTP_200_OK)
    

class SubmitCaseToAnalyst(APIView):
    permission_classes = [IsStorageClerk, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            submit_case_to_analyst(case=case, storage_clerk=request.user)
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case submitted to analyst"}, status=status.HTTP_200_OK)

