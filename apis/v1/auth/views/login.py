from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

##? Import Utils
from apis.utils.apiResponse import *
from apis.utils.token import create_JWT_token
from apis.utils import apiPermission

##? Import Serializer
from apis.v1.auth.serializers.LoginSerializer import LoginSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    ##? Ignore SessionAuthentication if you exempt CSRF
    authentication_classes = [JWTAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Update user activity
            user.last_activity = timezone.now()
            user.save(update_fields=['last_activity'])
            
            # Generate JWT token
            login(request, user)       
            token = create_JWT_token(user) 
            
            ##! User Groups
            user_groups = user.groups.all().values('id', 'name')
            groups = list(user_groups)
            
            ##! User Permissions
            # --- Collect user direct permissions ---
            user_permission_qs = user.user_permissions.all().values('id', 'name', 'codename')

            # --- Collect group permissions ---
            group_permission_qs = Permission.objects.filter(group__user=user).values('id', 'name', 'codename')

            # --- Combine both and remove duplicates by 'id' ---
            all_permissions_dict = {}
            for perm in list(user_permission_qs) + list(group_permission_qs):
                all_permissions_dict[perm['id']] = perm  # duplicates automatically overwritten

            permissions = list(all_permissions_dict.values())

            # --- Superuser override (optional) ---
            if user.is_superuser:
                permissions = list(Permission.objects.all().values('id', 'name', 'codename'))

            data = {
                'token': token,
                'message':'Login Success',
                'user': {
                    "id"          : user.id,
                    "name"        : user.name,
                    "first_name"  : user.first_name,
                    "last_name"   : user.last_name,
                    "email"       : user.email,
                    "phone"       : user.phone,
                    "is_verified" : user.is_verified,
                    "is_active"   : user.is_active,
                    "is_staff"    : user.is_staff,
                    "is_superuser": user.is_superuser,
                    "join_date"   : user.created_date_time,
                    "groups"      : groups,
                    "permissions" : permissions
                },
            }
            return api_success(data, message="Login successful.", status=200)

        return api_error({'errors': serializer.errors}, status=400, message="Validation error!")
            
        
     
class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    ##? Ignore SessionAuthentication if you exempt CSRF
    authentication_classes = [JWTAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            if not user.is_admin:
                return api_error({'errors': serializer.errors}, status=400, message="Your are not permitted to login!")

            # Update user activity
            user.last_activity = timezone.now()
            user.save(update_fields=['last_activity'])
            
            # Generate JWT token
            login(request, user)       
            token = create_JWT_token(user) 
            
            ##! User Groups
            user_groups = user.groups.all().values('id', 'name')
            groups = list(user_groups)
            
            ##! User Permissions
            # --- Collect user direct permissions ---
            user_permission_qs = user.user_permissions.all().values('id', 'name', 'codename')

            # --- Collect group permissions ---
            group_permission_qs = Permission.objects.filter(group__user=user).values('id', 'name', 'codename')

            # --- Combine both and remove duplicates by 'id' ---
            all_permissions_dict = {}
            for perm in list(user_permission_qs) + list(group_permission_qs):
                all_permissions_dict[perm['id']] = perm  # duplicates automatically overwritten

            permissions = list(all_permissions_dict.values())

            # --- Superuser override (optional) ---
            if user.is_superuser:
                permissions = list(Permission.objects.all().values('id', 'name', 'codename'))

            data = {
                'token': token,
                'message':'Login Success',
                'user': {
                    "id"          : user.id,
                    "name"        : user.name,
                    "first_name"  : user.first_name,
                    "last_name"   : user.last_name,
                    "email"       : user.email,
                    "phone"       : user.phone,
                    "is_verified" : user.is_verified,
                    "is_active"   : user.is_active,
                    "is_staff"    : user.is_staff,
                    "is_superuser": user.is_superuser,
                    "join_date"   : user.created_date_time,
                    "groups"      : groups,
                    "permissions" : permissions
                },
            }
            return api_success(data, message="Login successful.", status=200)

        return api_error({'errors': serializer.errors}, status=400, message="Validation error!")