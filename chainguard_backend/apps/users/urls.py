from django.urls import path
from . import views

urlpatterns = [
    path("users/register-user/", views.RegisterUserAPIView.as_view(), name="register-user"),
    path('users/login-user/', views.LoginUserAPIView.as_view(), name='login-user'),
    path('users/refresh-token/', views.RefreshTokenAPIView.as_view(), name='refresh-token'),
    path('users/logout/', views.LogoutAPIView.as_view(), name='logout-user'),
    path('users/', views.UserListAPIView.as_view(), name='users'),
    path('users/<uuid:pk>/', views.UserRetrieveAPIView.as_view(), name='users-detail'),
    path('users/<uuid:pk>/assign-role/', views.AssignRoleAPIView.as_view(), name='assign-role'),
    path('users/me/complete-profile/', views.CompleteProfileAPIView.as_view(), name='complete-profile'),
    path('users/me/update-profile/', views.UpdateUserAPIView.as_view(), name='update-profile'),
]