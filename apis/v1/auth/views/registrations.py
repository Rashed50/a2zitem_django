from rest_framework.views import APIView
from rest_framework import generics, status
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import random
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
        IsAuthenticated, 
    )

from django.contrib.auth import get_user_model
User = get_user_model()

## Custom Import
from users.models import UserOTP 

from core.utils.api_utils import api_success, api_error, create_JWT_token
from core.services.email_send import html_mail_sender
from core.services.sms_send import sms_sender 

from rest_framework import serializers
from apis.v1.auth.serializers.RegistrationSerializer import (
        UserRegistrationSerializer, 
        UserRegistrationVerifySerializer,
    )


# from apis.users.utils import OTP_Send


"""
    User Registration
    @Rakib
"""
# class UserRegistrationView(APIView):
#     def post(self, request, format=None):
#         user_serializer = UserRegistrationSerializer(data=request.data)

#         if user_serializer.is_valid():
#             user_serializer.save()

#             # Get the user by email
#             user = User.objects.filter(email=user_serializer.validated_data['email']).first()
#             otp = UserOTP.objects.filter(user = user).first()
#             if otp:
#                 msg = {
#                     'token': otp.token, 
#                     'message': 'Registration Successful. Please check your email or phone to verify your account.'}
#                 return api_success(user_serializer.data, status=201, message=msg)
#             else:
#                 return api_error({'message': 'User not found'}, status=404)

#         return api_error({'errors': user_serializer.errors}, status=422, message="Validation error!")




class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "success": True,
            "message": "User registered successfully",
            "data": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "gender": user.gender,
                "religion": user.religion,
                "dob": user.dob,
                "auth_provider": user.auth_provider,
                "language_preference": user.language_preference,
                "timezone": user.timezone,
                "two_factor_enabled": user.two_factor_enabled
            }
        }, status=status.HTTP_201_CREATED)
