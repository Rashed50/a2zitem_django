from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string


##? Utils Import
from core.services.email_send import html_mail_sender

def send_forgot_password_otp_email(user, otp_obj):
    try:
        otp_str = str(otp_obj.otp).zfill(6)
        
        html_content = render_to_string(
            'emails/OTP_Varification_Email.html',
            {
                ##? Core OTP Data
                "user"        : user,
                "otp"         : otp_str,
                "otp_digits"  : list(otp_str),
                "otp_token"   : otp_obj.token,
                "otp_timeout" : settings.OTP_TIMEOUT,
                "now"         : timezone.now(),
                
                ##? Email Content - Specific for Forgot Password
                "email_title"    : "Recover Your Account",
                "email_subtitle" : "We received a request to reset your password",
                "email_purpose"  : "reset your password",
            }
        )

        sent = html_mail_sender(
            subject      = 'Recover your account.', ## subject
            html_content = html_content,            ## html_content
            to           = [user.email],            ## to
        )

        return bool(sent)   # ✅ True / False

    except Exception as e:
        print("=============================")
        print("Forgot Password OTP Email Error:", str(e))
        print("=============================")
        return False



