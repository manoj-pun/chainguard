from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from apps.common.permissions import IsAnalyst, IsProfileComplete
from rest_framework.permissions import IsAuthenticated
from .serializers import FindingCreateSerializer, FindingListSerializer, FindingDetailSerializer
from .models import Finding
from .services import create_finding
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string


"""API end point to list and create findings"""
class FindingListCreateAPIView(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnalyst(), IsProfileComplete()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FindingCreateSerializer
        return FindingListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "ANALYST":
            return Finding.objects.filter(analyst=user)
        return Finding.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        finding = create_finding(
            analyst=request.user,
            **serializer.validated_data
        )
        return Response(FindingListSerializer(finding).data, status=status.HTTP_201_CREATED)


"""API end point to view findings with id"""
class FindingDetailAPIView(RetrieveAPIView):
    serializer_class = FindingDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ANALYST":
            return Finding.objects.filter(analyst=user)
        return Finding.objects.all()
    

"""API end point to download findings"""
class FindingDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfileComplete]

    def get(self, request, pk):
        finding = get_object_or_404(Finding, finding_id=pk)

        html_string = render_to_string('findings/finding_pdf.html', {
            'finding': finding,
            'evidence': finding.evidence,
            'analyst': finding.analyst,
        })

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="finding_{finding.version_number}.pdf"'
        return response