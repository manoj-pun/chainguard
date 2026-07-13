from .serializers import (
    CaseCreateSerializer, 
    CaseListSerializer,
    CaseDetailSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .models import Case
from apps.common.permissions import IsOfficer, IsProfileComplete, IsStorageClerk, IsAnalyst, IsSupervisor
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import (
    create_case, 
    submit_case_to_storage, 
    acknowledge_case, 
    submit_case_to_analyst, 
    submit_findings,
    send_case_to_court, 
    close_case
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .pagination import CasePagination
from rest_framework.pagination import LimitOffsetPagination
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers
from rest_framework.filters import SearchFilter
from django.core.cache import cache

"""Create and list cases
    Create can only be done by officer
    List can only be done supervisor and officer can only list his cases
"""
class CaseCreateAPIView(ListCreateAPIView):
    pagination_class = CasePagination
    # filter_backends = [SearchFilter]
    # search_fields = ["title"]

    """Implementing caching"""
    def get_cache_key(self,user):
        if user.role == "OFFICER":
            return f"case_list:OFFICER:{user.pk}"
        return f"case_list:{user.role}"
    
    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(request.user)
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key,response.data,timeout=60*5)
        return response

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOfficer(),IsProfileComplete()]
        return [IsAuthenticated()]
        # return [AllowAny()] #to check the pagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CaseCreateSerializer
        return CaseListSerializer

    def get_queryset(self):
        user = self.request.user
        # if not user.is_authenticated:
        #     return Case.objects.all() #to check the pagination
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


"""API end point for viewing case with id""" 
class CaseDetailAPIView(RetrieveAPIView):
    serializer_class = CaseDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        user = self.request.user
        if user.role == "SUPERVISOR":
            return Case.objects.all()
        return Case.objects.filter(officer = user)


"""API end point for submitting case to storage
    Only officer can do
"""
class SubmitCaseToStorageAPIView(APIView):
    permission_classes = [IsOfficer, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk, officer=request.user)

        try:
            submit_case_to_storage(case=case, officer=request.user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Case submitted to storage."}, status=status.HTTP_200_OK)
    

"""API end point for acknowledging the case
    Only storage clerk can do
"""
class AcknowledgeCaseAPIView(APIView):
    permission_classes = [IsStorageClerk, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            acknowledge_case(case=case, storage_clerk=request.user)
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case Acknowledged"}, status=status.HTTP_200_OK)
    

"""API end point for submitting the case to analyst
    Only storage clerk can do
"""
class SubmitCaseToAnalystAPIView(APIView):
    permission_classes = [IsStorageClerk, IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            submit_case_to_analyst(case=case, storage_clerk=request.user)
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case submitted to analyst"}, status=status.HTTP_200_OK)
    

"""API end point to submit findings
    Only analyst can do
"""
class SubmitFindingsAPIView(APIView):
    permission_classes = [IsAnalyst,IsProfileComplete]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            submit_findings(case=case, analyst=request.user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Findings submitted to supervisor"}, status=status.HTTP_200_OK)


"""API end point to send case to court
    Only supervisor can do
"""
class SendCaseToCourtAPIView(APIView):
    permission_classes = [IsSupervisor]

    def post(self,request,pk):
        case = get_object_or_404(Case, case_id=pk)

        try:
            send_case_to_court(case=case, supervisor=request.user)
        except ValueError as e:
            return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case sent to court"}, status=status.HTTP_200_OK)
    

"""API end point for closing case
    Only supervisor can do
"""
class CloseCaseAPIView(APIView):
    permission_classes = [IsSupervisor]

    def post(self,request,pk):
        case = get_object_or_404(Case,case_id=pk)

        try:
            close_case(case=case, supervisor=request.user)
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail":"Case Closed"},status=status.HTTP_200_OK)

