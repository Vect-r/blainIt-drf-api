# serializers.py
from rest_framework import serializers

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)

    def validate_phone(self, value):
        # Basic validation to ensure the phone number only contains digits.
        # You could also add a regex here to enforce a specific country code format.
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    otp = serializers.CharField(max_length=6, required=True)