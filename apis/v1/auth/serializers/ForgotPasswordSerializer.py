from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password, ValidationError

##? Utils Import
from apis.utils.field_error_messages import get_field_error_messages

##? Services Import
from apis.v1.auth.services.query.userQuery import getUser

##? Models Import
User = get_user_model()
from users.models import UserOTP


class ForgotPasswordSendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required    = True,
        write_only  = True,
        max_length  = 255,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('Email', 'EmailField'),
    )
    
    def validate_email(self, value):
        
        ##? ✅ User Validation
        user = getUser(email=value)   
        
        ##? 🔒 Check if an active OTP already exists
        active_otp_exists = UserOTP.objects.filter(
            user           = user,
            is_otp_used        = False,
            expires_at__gt = timezone.now()
        ).exists()
        
        if active_otp_exists:
            raise serializers.ValidationError(
                _("An OTP has already been sent. Please wait until it expires.")
            )
        
        self.context['user'] = user
        return value

class ForgotPasswordVerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(
        required    = True,
        write_only  = True,
        max_length  = 6,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('OTP', 'CharField'),
    )
    
    token = serializers.CharField(
        required    = True,
        write_only  = True,
        allow_blank = False,
        allow_null  = False,
        max_length  = 64,
        error_messages = get_field_error_messages('Token', 'CharField'),
    )

    def validate(self, attrs):
        token = attrs.get("token")
        otp   = attrs.get("otp")
        
        try:
            user_otp = UserOTP.objects.select_related("user").get(
                token   = token,
                otp     = otp,
                is_otp_used = False,
            )
            
            if user_otp.is_otp_used:
                raise serializers.ValidationError({
                    "otp": _("OTP has already been used.")
                })
        except UserOTP.DoesNotExist:
            raise serializers.ValidationError({
                "otp": _("Invalid OTP!")
            })
            
        # ⏳ Expiry check
        if user_otp.is_otp_expired:
            raise serializers.ValidationError({
                "otp": _("OTP has expired.")
            })
            
        attrs["user"]     = user_otp.user
        attrs["user_otp"] = user_otp
        return attrs


class ForgotPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required    = True,
        write_only  = True,
        max_length  = 255,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('Email', 'EmailField'),
    )
    token = serializers.CharField( 
        required    = True,
        write_only  = True,
        max_length  = 64,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('Token', 'CharField'),
    )
    new_password = serializers.CharField(
        required    = True,
        write_only  = True,
        max_length  = 30,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('New Password', 'CharField'),
    )
    confirm_password = serializers.CharField(
        required    = True,
        write_only  = True,
        max_length  = 30,
        allow_null  = False,
        allow_blank = False,
        error_messages = get_field_error_messages('Confirm Password', 'CharField'),
    )

    def validate(self, attrs):
        email = attrs.get("email")
        token = attrs.get("token")
        new_password     = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        ## 1️⃣ User validation (active + verified)
        user = getUser(email=email)

        ## 2️⃣ Find OTP record using token
        try:
            user_otp = UserOTP.objects.get(
                user    = user,
                token   = token,
                is_otp_used   = True,
                is_token_used = False
            )
        except UserOTP.DoesNotExist:
            raise serializers.ValidationError({
                "token": _("Invalid or expired token.")
            })

        # 4️⃣ Check token expiry (OTP_TOKEN_TIMEOUT)
        if user_otp.is_token_expired:
            raise serializers.ValidationError({
                "token": _("Token has expired. Please restart the password reset process.")
            })

        # 5️⃣ Password match check
        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": _("Passwords do not match.")
            })

        # 6️⃣ Password strength validation
        try:
            validate_password(new_password, user=user)
        except Exception as e:
            raise serializers.ValidationError({
                "new_password": list(e.messages)
            })

        attrs["user"] = user
        attrs["user_otp"] = user_otp
        return attrs


class ForgotPasswordResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        ##? ✅ User Validation
        user = getUser(email=value)
        
        ##? 🔒 Check if an active OTP already exists
        active_otp_exists = UserOTP.objects.filter(
            user           = user,
            is_otp_used        = False,
            expires_at__gt = timezone.now()
        ).exists()
        
        if active_otp_exists:
            raise serializers.ValidationError(
                _("An OTP has already been sent. Please wait until it expires.")
            )
            
        self.context['user'] = user
        return value
