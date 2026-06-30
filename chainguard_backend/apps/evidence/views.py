from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from .serializers import (
    EvidenceCreateSerializer, 
    EvidenceListSerializer, 
    EvidenceDetailSerializer,
    EvidenceFileCreateSerializer,
    EvidenceFileListSerializer,
    EvidenceFileDetailSerializer
)
from .models import Evidence, EvidenceFile
from apps.common.permissions import IsOfficer, IsSuperVisorOrOfficer, IsProfileComplete
from .services import create_evidence, create_evidence_file
from rest_framework.response import Response
from rest_framework import status

class EvidenceListCreateAPIView(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOfficer(), IsProfileComplete()]
        return [IsSuperVisorOrOfficer()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return Evidence.objects.all()
        return Evidence.objects.filter(officer=user)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return EvidenceCreateSerializer
        return EvidenceListSerializer
    
    """Use the below function if you know which data to pass"""
    # def create(self,request,*args,**kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     evidence = create_evidence(
    #         officer = self.request.user,
    #         validated_data = serializer.validated_data
    #     )

    #     return Response(
    #         EvidenceListSerializer(evidence).data, status=status.HTTP_201_CREATED
    #     )
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        evidence = create_evidence(
            officer = self.request.user,
            **serializer.validated_data
        )

        return Response(
            EvidenceListSerializer(evidence).data, status=status.HTTP_201_CREATED
        )
    

class EvidenceDetailAPIView(RetrieveAPIView):
    serializer_class = EvidenceDetailSerializer
    permission_classes = [IsSuperVisorOrOfficer, IsProfileComplete]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return Evidence.objects.all()
        return Evidence.objects.filter(officer=user)
    

class EvidenceFileListCreateAPIVIew(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOfficer(), IsProfileComplete()]
        return [IsSuperVisorOrOfficer()]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return EvidenceFileCreateSerializer
        return EvidenceFileListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return EvidenceFile.objects.all()
        return EvidenceFile.objects.filter(evidence__officer=user)
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
         
        evidence_file = create_evidence_file(
            officer = self.request.user,
            **serializer.validated_data
        )

        return Response(
            EvidenceFileListSerializer(evidence_file).data,
            status=status.HTTP_201_CREATED
        )
    

class EvidenceFileDetailAPIView(RetrieveAPIView):
    serializer_class = EvidenceFileDetailSerializer
    permission_classes = [IsSuperVisorOrOfficer, IsProfileComplete]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return EvidenceFile.objects.all()
        return EvidenceFile.objects.filter(evidence__officer=user)


