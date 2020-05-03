from django.urls import path

from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path("", RegisterView.as_view(), name="rest_register"),
    path("verify-email/<str:key>/", VerifyEmailView.as_view(), name="rest_verify_email"),
]