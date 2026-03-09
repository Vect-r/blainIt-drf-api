# users/views.py
import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Save OTP in cache with a 5-minute expiration (300 seconds)
        cache.set(f"otp_{phone_number}", otp, timeout=300)

        # TODO: Integrate SMS provider (Twilio, AWS SNS, Msg91) to actually send the OTP
        print(f"Mock SMS - OTP for {phone_number} is {otp}")

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_otp = request.data.get('otp')

        if not phone_number or not user_otp:
            return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(f"otp_{phone_number}")

        if cached_otp is None:
            return Response({"error": "OTP has expired or does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if cached_otp == user_otp:
            # OTP is correct. Get or create the user (auto-registration)
            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
            
            # Clear the OTP from cache so it can't be reused
            cache.delete(f"otp_{phone_number}")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_new_user": created
            }, status=status.HTTP_200_OK)
            
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)