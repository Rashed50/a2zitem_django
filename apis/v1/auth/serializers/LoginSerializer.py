from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

##? Model Import
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    password       = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email_or_phone = attrs.get("email_or_phone")
        password       = attrs.get("password")

        if not email_or_phone:
            raise serializers.ValidationError(_("Email/Phone is required."))
        
        if not password:
            raise serializers.ValidationError(_("Password is required."))

        # Check if user exists by email or phone
        try:
            if '@' in email_or_phone:
                user = User.objects.get(email__iexact=email_or_phone)
            else:
                user = User.objects.get(phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email_or_phone": [
                        _("User is not registered with us. Please register first.")
                    ]
                }
            )

        # Authenticate user
        # user = authenticate(email=user.email, password=password)
        user = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()
        
        if user:
            if user.check_password(password) == False:
                raise serializers.ValidationError({"password":[_("Password is incorrect.")]})
            
            elif not user.is_active:
                raise serializers.ValidationError({"email_or_phone": _("This account is inactive.")})
            
            elif not user.is_verified:
                raise serializers.ValidationError({"email_or_phone": _("This account is not verified.")})
            
            else:
                usr = authenticate( email = user.email, password = password)
                attrs["user"] = usr
                return attrs
        
            
        elif not user:
            raise serializers.ValidationError(_("Invalid credentials or inactive account."))

        elif not user.is_active:
            raise serializers.ValidationError(_("This account is inactive."))

        raise serializers.ValidationError("Invalid login credentials!")







# class UserLoginSerializer(serializers.Serializer):
#     email_or_phone = serializers.CharField()
#     password       = serializers.CharField(write_only=True)

#     def validate(self, atts):
#         email_or_phone = atts.get("email_or_phone")
#         password = atts.get("password")

#         user = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()

#         if user:
#             if user.check_password(password) == False:
#                 raise serializers.ValidationError("Password is incorrect!")
#             elif not user.is_active:
#                 raise serializers.ValidationError("The user is disabled!")
#             else:
#                 usr = authenticate( email = user.email, password = password)
#                 atts["user"] = usr
#                 return atts
        
#         raise serializers.ValidationError("Invalid login credentials!")

        