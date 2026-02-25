from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email, MinLengthValidator
from django.contrib.auth.password_validation import validate_password, ValidationError

##? Utils Import
from apis.utils.field_error_messages import get_field_error_messages
from users.validators import DateOfBirthValidator, ImageValidator

##? Services Import
from apis.v1.auth.services.query.userQuery import getUser

##? Models Import
User = get_user_model()
from users.models import UserDetails, UserOTP, UserImageGallery
from core.models.religion_model import Religion, ReligionDenomination

##? Serializers Import
from apis.v1.common.religion.serializers.ReligionSerializer import ReligionSerializer
from apis.v1.common.religion.serializers.ReligionDenominationSerializer import ReligionDenominationSerializer

##! OTP Verification
class IncompleteProfileVarifyOTPSerializer(serializers.Serializer):
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
    
    
##! Password Reset 
class IncompleteProfilePasswordResetSerializer(serializers.Serializer):
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
    

##! Resend OTP 
class IncompleteProfileResendOTPSerializer(serializers.Serializer):
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
    

##! Incomplete Profile Update
class IncompleteProfileUpdateSerializer(serializers.ModelSerializer):
    religion = ReligionSerializer(read_only=True)
    
    religion_id = serializers.PrimaryKeyRelatedField(
        source      = "religion",
        queryset    = Religion.objects.all(),
        write_only  = True,
        required    = True,
        allow_null  = False,
        error_messages = get_field_error_messages('Religion', 'PrimaryKeyRelated'),
    )
    
    address = serializers.CharField(
        source      = "details.address",
        required    = False,
        allow_null  = True,
        allow_blank = True,
        max_length  = 500,
        error_messages = get_field_error_messages('Address', 'CharField'),
    )
    
    bio = serializers.CharField(
        source      = "details.bio",
        required    = False,
        allow_null  = True,
        allow_blank = True,
        max_length  = 1000,
        error_messages = get_field_error_messages('Bio', 'CharField'),
    )
    class Meta:
        model  = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'dob',
            'gender',
            
            ##? Religion and Religion Denomination Fields
            'religion', 'religion_id',
            
            ##? Profile Image
            'image',
            
            ##? Extra Fields
            'address',
            'bio',
        ]
        
        extra_kwargs = {
            'first_name': {
                'required'       : True, 
                'allow_null'     : False, 
                'allow_blank'    : False,
                'validators'     : [MinLengthValidator(2)],
                'error_messages' : get_field_error_messages('First Name', 'CharField')
            },
            'last_name' : {
                'required'       : True, 
                'allow_null'     : False, 
                'allow_blank'    : False,
                'validators'     : [MinLengthValidator(2)],
                'error_messages' : get_field_error_messages('Last Name', 'CharField')
            },
            'phone'     : {
                'required'       : True, 
                'allow_null'     : False, 
                'allow_blank'    : False,
                'validators'     : [MinLengthValidator(10)],
                'error_messages' : get_field_error_messages('Phone', 'CharField')
            },
            'dob'       : {
                'required'       : True, 
                'allow_null'     : False,
                'validators'     : [DateOfBirthValidator],
                'error_messages' : get_field_error_messages('Date of Birth', 'DateField')
            },
            'gender'    : {
                'required'       : True, 
                'allow_null'     : False, 
                'allow_blank'    : False,
                'error_messages' : get_field_error_messages('Gender', 'CharField')
            },
            'image': {
                'required'   : True,
                'allow_null' : False,
                'validators' : [ImageValidator],
                'error_messages' : get_field_error_messages('Image', 'ImageField')
            },
        }
        
    def validate_phone(self, value):
        user = self.instance
        if value != user.phone:
            if User.objects.filter(phone=value).exclude(pk=user.pk).exists():
                raise serializers.ValidationError(_("This phone number is already in use."))
        return value

    def update(self, instance, validated_data):
        request    = self.context.get('request')
        image_file = validated_data.get('image', None)
        
        ##? Extract nested details
        details_data = {}
        if 'details' in validated_data:
            details_nested = validated_data.pop('details')
            if 'address' in details_nested:
                details_data['address'] = details_nested.get('address')
            if 'bio' in details_nested:
                details_data['bio'] = details_nested.get('bio')
                
        try:
            with transaction.atomic():
        
                ##? User Data Update 
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                if image_file:
                    profile_gallery_image = UserImageGallery.objects.create(
                        user       = instance,
                        image_type = UserImageGallery.ImageType.PROFILE,
                        image      = image_file, 
                    )
                    
                    ##? Profile Image set on UserDetails
                    user_details, _ = UserDetails.objects.get_or_create(user=instance)
                    user_details.profile_image = profile_gallery_image
                    user_details.save()
                
                ##? Update UserDetails if needed
                if any(details_data.values()):  
                    user_details, _ = UserDetails.objects.get_or_create(user=instance)
                    for attr, value in details_data.items():
                        if value is not None:  
                            setattr(user_details, attr, value)
                    user_details.save()
                
            return instance
        except Exception as e:
            raise serializers.ValidationError({
                "non_field_errors": [_("An error occurred while updating the profile. Please try again.")]
            })
            
            