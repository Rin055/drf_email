from django.urls import path
from .views import SendEmailView, PasswordResetRequestViewSet, PasswordResetConfirmViewSet

urlpatterns = [
    path('send-email/', SendEmailView.as_view()),
    path("password-reset/", PasswordResetRequestViewSet.as_view({'post': 'create'}), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmViewSet.as_view({'post': 'create'}), name="password-reset-confirm"),
]
