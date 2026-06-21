from django.urls import path
from . import views

urlpatterns = [
    path("users/register-user/", views.RegisterUserAPIView.as_view())
]