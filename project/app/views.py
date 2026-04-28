from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import EmailSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer


class SendEmailView(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            subject = data['subject']
            message = data['message']
            sender = data['sender_email']

            recipients = data.get('recipient_emails', ['giokhomaa@gmail.com'])

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=recipients,
                reply_to=[sender]
            )

            files = request.FILES.getlist('attachments')
            for file in files:
                email.attach(file.name, file.read(), file.content_type)

            try:
                email.send()
                return Response(
                    {"detail": "Email sent successfully!"},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"error": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetRequestViewSet(ViewSet):
    serializer_class = PasswordResetSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Token generation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Password reset URL generation
            reset_url = request.build_absolute_uri(
                f"/password-reset-confirm/{uid}/{token}/"
            )

            # Send email
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Password reset email sent successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetConfirmViewSet(ViewSet):
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successful"},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )