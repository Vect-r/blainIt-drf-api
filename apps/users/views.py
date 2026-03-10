# views.py
import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  # Ensure this points to your custom User model
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .tokens import CustomRefreshToken 

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        
        # This automatically checks if the phone field is present and valid
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Save OTP in cache with a 5-minute expiration (300 seconds)
            cache.set(f"otp_{phone}", otp, timeout=300)

            # TODO: Integrate your SMS provider here
            print(f"Mock SMS - OTP for {phone} is {otp}")

            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        
        # If the data was invalid, return the specific errors automatically
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user_otp = serializer.validated_data['otp']

            cached_otp = cache.get(f"otp_{phone}")

            if cached_otp is None:
                return Response({"error": "OTP has expired or does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if cached_otp == user_otp:
                user, created = User.objects.get_or_create(phone=phone)
                cache.delete(f"otp_{phone}")

                # Use your custom token class here instead of the default one
                refresh = CustomRefreshToken.for_user(user)

                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "is_new_user": created
                }, status=status.HTTP_200_OK)
                
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)