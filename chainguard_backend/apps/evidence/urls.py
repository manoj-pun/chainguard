from django.urls import path
from . import views

urlpatterns = [
    path("evidence/", views.EvidenceListCreateAPIView.as_view()),
    path("evidence/<uuid:pk>/", views.EvidenceDetailAPIView.as_view()),
    path("evidencefile/", views.EvidenceFileListCreateAPIVIew.as_view()),
    path("evidencefile/<uuid:pk>/", views.EvidenceFileDetailAPIView.as_view()),
]