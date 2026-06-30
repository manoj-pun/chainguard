from django.urls import path
from . import views

urlpatterns = [
    path("findings/", views.FindingListCreateAPIView.as_view()),
    path("findings/<uuid:pk>/", views.FindingDetailAPIView.as_view()),
    path("findings/<uuid:pk>/download/", views.FindingDownloadAPIView.as_view()),
]