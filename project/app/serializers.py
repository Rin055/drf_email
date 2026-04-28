from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    sender_email = serializers.EmailField()


    recipient_emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )

    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )