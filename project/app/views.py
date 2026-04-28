from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from .serializers import EmailSerializer


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