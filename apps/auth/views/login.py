import json, random, time
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views import View, generic
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('dashboard:home')  
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email_or_phone = request.POST.get('email_or_phone')
        password       = request.POST.get('password')
        remember_me    = request.POST.get('remember_me') == 'on'
        fcm_token      = request.POST.get('fcm_token', '').strip()
        signup_ip      = request.POST.get('signup_ip')
        signup_source  = request.POST.get('signup_source', 'web')
        
        # print("-----------------------------")
        # print("Email/Phone:", email_or_phone)
        # print("Password:", password)
        # print("Remember Me:", remember_me)
        # print("Client IP:", signup_ip)
        # print("FCM/Device Token:", fcm_token)
        # print("Signup Source:", signup_source)
        # print("User Agent:", request.META.get('HTTP_USER_AGENT', ''))
        # print("-----------------------------")

        # Validate required fields
        if not email_or_phone or not password:
            return render(request, self.template_name, {
                'error'          : 'Email/Phone and password are required.',
                'error_type'     : 'Validation',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })

        # Determine if input is email or phone
        is_email = self.is_valid_email(email_or_phone)
        
        # Find user by email or phone
        try:
            if is_email:
                user = User.objects.get(email=email_or_phone)
            else:
                user = User.objects.get(phone=email_or_phone)
                
        except User.DoesNotExist:
            error_field = "email" if is_email else "phone number"
            return render(request, self.template_name, {
                'error'          : f'Invalid {error_field}.',
                'error_type'     : 'EmailOrPhone',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })
            
        # check user is admin/superuser
        if not (user.is_admin or user.is_superuser):
            return render(request, self.template_name, {
                'error'          : 'You are not authorized to log in.',
                'error_type'     : 'Authorization',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })

        # Check if user is active
        if not user.is_active:
            return render(request, self.template_name, {
                'error'          : 'Your account has been disabled. Please contact administrator.',
                'error_type'     : 'Disabled',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })

        # Check if account is locked due to failed login attempts
        if user.lockout_until and timezone.now() < user.lockout_until:
            remaining_time = user.lockout_until - timezone.now()
            minutes_remaining = int(remaining_time.total_seconds() / 60)
            return render(request, self.template_name, {
                'error'          : f'Account temporarily locked. Try again in {minutes_remaining} minutes.',
                'error_type'     : 'Locked',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })

        # Authenticate user - use email as username for authentication
        auth_user = authenticate(request, username=user.email, password=password)
        
        if auth_user is not None:
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.lockout_until = None
            user.last_activity = timezone.now()
            
            # Update FCM device token if provided
            fcm_token = request.POST.get('fcm_token')
            if fcm_token:
                user.fcm_device_token = fcm_token
            
            # Update signup IP and source if not set (for new users)
            if not user.signup_ip:
                user.signup_ip = self.get_client_ip(request)
            if not user.signup_source:
                user.signup_source = 'web'
                
            user.save()
            
            # Handle Remember Me functionality using settings
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            
            # Login the user
            auth_login(request, auth_user)
            
            # Redirect to next URL or home page
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
            
        else:
            # Increment failed login attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts for 3 minutes
            if user.failed_login_attempts >= 5:
                user.lockout_until = timezone.now() + timezone.timedelta(minutes=3)
                error_message = 'Account locked due to multiple failed attempts. Try again in 3 minutes.'
            else:
                attempts_remaining = 5 - user.failed_login_attempts
                error_message = f'Invalid password. {attempts_remaining} attempts remaining.'
            
            user.save()
            
            return render(request, self.template_name, {
                'error'          : error_message,
                'error_type'     : 'Password',
                'email_or_phone' : email_or_phone,
                'password'       : password
            })

    def is_valid_email(self, value):
        """Check if the provided value is a valid email"""
        try:
            validate_email(value)
            return True
        except ValidationError:
            return False

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# class LoginView(View):
#     template_name = "login.html"

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             next_url = request.GET.get('next')
#             if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
#                 return redirect(next_url)
#             return redirect('dashboard:home')  
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         email       = request.POST.get('email')
#         password    = request.POST.get('password')
#         remember_me = request.POST.get('remember_me') == 'on'  # Checkbox returns 'on' when checked
        
#         print("-----------------------------")
#         print("Email:", email)
#         print("Password:", password)
#         print("Remember Me:", remember_me)
#         print("-----------------------------")

#         # Validate required fields
#         if not email or not password:
#             return render(request, self.template_name, {
#                 'error'      : 'Email and password are required.',
#                 'error_type' : 'Validation',
#                 'email'      : email,
#                 'password'   : password
#             })

#         # Find user by email
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return render(request, self.template_name, {
#                 'error'      : 'Invalid email address.',
#                 'error_type' : 'Email',
#                 'email'      : email,
#                 'password'   : password
#             })

#         # Authenticate user
#         auth_user = authenticate(request, username=email, password=password)
        
#         if auth_user is not None:
#             # Handle Remember Me functionality using settings
#             if remember_me:
#                 # Use SESSION_COOKIE_AGE from settings (14 days)
#                 request.session.set_expiry(settings.SESSION_COOKIE_AGE)
#             else:
#                 # Session will expire when browser closes
#                 request.session.set_expiry(0)
            
#             # Login the user
#             auth_login(request, auth_user)
            
#             # Redirect to next URL or home page
#             next_url = request.GET.get('next')
#             if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
#                 return redirect(next_url)
#             return redirect(settings.LOGIN_REDIRECT_URL)  # Use from settings
#         else:
#             # Invalid password
#             return render(request, self.template_name, {
#                 'error'      : 'Invalid password.',
#                 'error_type' : 'Password',
#                 'email'      : email,
#                 'password'   : password
#             })