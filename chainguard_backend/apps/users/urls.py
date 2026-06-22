from django.urls import path
from . import views

urlpatterns = [
    path("users/register-user/", views.RegisterUserAPIView.as_view(), name="register-user"),
    path('users/login-user/', views.LoginUserAPIView.as_view(), name='login-user'),
]