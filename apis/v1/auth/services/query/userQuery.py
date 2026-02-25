from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

##? Models Import
User = get_user_model()
from users.models import UserOTP


def CreateUserOTP(user):
    ##? 🔒 Check if an active OTP already exists
    active_otp_exists = UserOTP.objects.filter(
        user           = user,
        is_otp_used    = False,
        expires_at__gt = timezone.now()
    ).exists()
    
    if active_otp_exists:
        raise serializers.ValidationError(
            _("An OTP has already been sent. Please wait until it expires.")
        )
            
    ## Deactivate unused OTPs
    UserOTP.objects.filter(
        user           = user,
        is_otp_used    = False,
        is_token_used  = False,
        expires_at__gt = timezone.now()
    ).update(is_otp_used=True, is_token_used=True)

    ## Create new OTP
    otp_obj = UserOTP.objects.create(user=user)
    return otp_obj


def getUser(*, user=None, user_id=None, email=None):
    """
##?  Docstring for getUser
##* :param user    : user = getUser(user=request.user)
##* :param user_id : user = getUser(user_id=request.data["user_id"])
##* :param email   : user = getUser(email="test@example.com")
    """
    # --- Ensure only ONE identifier is provided ---
    provided = [user, user_id, email]
    if sum(x is not None for x in provided) != 1:
        raise ValidationError(
            _("Provide exactly one of: user, user_id, or email.")
        )

    # --- Resolve user ---
    if user:
        if not isinstance(user, User):
            raise ValidationError(_("Invalid user object provided."))
        resolved_user = user

    elif user_id:
        try:
            resolved_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({
                "user_id": _("User with this ID does not exist.")
            })

    elif email:
        try:
            resolved_user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError({
                "email": _("User with this email does not exist.")
            })

    # --- Validation rules ---
    if not resolved_user.is_active:
        raise ValidationError({
            "user": _("This account is inactive. Please contact support.")
        })

    if not resolved_user.is_verified:
        raise ValidationError({
            "user": _("This account is not verified. Please verify your account first.")
        })

    return resolved_user










# def getUser(email):
#     try:
#         user = User.objects.get(email__iexact=email)
#     except User.DoesNotExist:
#         raise ValidationError({
#             "email": _("User with this email does not exist.")
#         })

#     if not user.is_active:
#         raise ValidationError({
#             "email": _("This account is inactive. Please contact support.")
#         })

#     if not user.is_verified:
#         raise ValidationError({
#             "email": _("This account is not verified. Please verify your account first.")
#         })

#     return user





