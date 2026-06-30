from django.urls import path
from . import views

urlpatterns = [
    path("cases/", views.CaseCreateAPIView.as_view()),
    path("cases/<uuid:pk>/", views.CaseDetailAPIView.as_view()),

    path("cases/<uuid:pk>/submit-case-to-storage/", views.SubmitCaseToStorageAPIView.as_view()),
    path("cases/<uuid:pk>/acknowledge-case/", views.AcknowledgeCaseAPIView.as_view()),
    path("cases/<uuid:pk>/submit-case-to-analyst/", views.SubmitCaseToAnalystAPIView.as_view()),
    path("cases/<uuid:pk>/submit-findings/", views.SubmitFindingsAPIView.as_view()),
    path("cases/<uuid:pk>/submit-case-to-court/", views.SendCaseToCourtAPIView.as_view()),
    path("cases/<uuid:pk>/close-case/", views.CloseCaseAPIView.as_view()),
]