from django.urls import path
from . import views

urlpatterns = [
    path("cases/", views.CaseCreateAPIView.as_view())
]