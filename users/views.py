from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, SeatSerializer, ReservationSerializer
from .models import User, Seat, Reservation, ClassRoom

# Existing view
def all_user(request):
    return HttpResponse('Returning all users')

# New Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user.email_verified_at:
                return Response(
                    {"error": "Please verify your email before logging in"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            
            return Response({
                "message": "Login successful",
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send verification email
            verification_token = self._generate_verification_token(user)
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{verification_token}"
            
            send_mail(
                'Verify your email',
                f'Please click the following link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({
                "message": "Registration successful. Please check your email to verify your account.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_verification_token(self, user):
        # In a real implementation, you would use a proper token generation method
        # This is just a simple example
        return f"{user.id}-{user.email}-{timezone.now().timestamp()}"
    
class AdminDashboardStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        empty_seats_count = Seat.objects.filter(is_available=False).count()
        available_seats_count = Seat.objects.filter(is_available=True).count()
        empty_classroom_count = ClassRoom.objects.filter(is_available=False).count()
        available_classroom_count = ClassRoom.objects.filter(is_available=True).count()

        data = {
            "empty_seats_count": empty_seats_count,
            "available_seats_count": available_seats_count,
            "empty_classroom_count": empty_classroom_count,
            "available_classroom_count": available_classroom_count,
        }

        return Response(data)