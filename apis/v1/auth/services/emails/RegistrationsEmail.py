from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string

from django.conf import settings

##? Utils Import
from core.services.email_send import html_mail_sender

def send_registration_success_email(user):
    """
    Send registration success email with credentials and login link
    """
    try:
        html_content = render_to_string(
            'emails/RegistrationSuccessEmail.html',
            {
                'user'             : user,
                'default_password' : settings.DEFAULT_USER_PASSWORD,  
                'login_url'        : 'http://localhost:3000/login',  
                'email_title'      : 'Welcome to ABC Limited!',
                'company_name'     : 'ABC Limited',
                'now'              : timezone.now(),
            }
        )

        sent = html_mail_sender(
            subject      = 'Your Account Has Been Created Successfully!',      ## subject
            html_content = html_content,                      ## html_content
            to           = [user.email],                      ## to
            # cc           = ['hello@nusratgeek.com'],        ## cc
        )

        return bool(sent)   # ✅ True / False

    except Exception as e:
        print("=============================")
        print("Registration Email Error:", str(e))
        print("User:", user.email if user else "Unknown")
        print("=============================")
        return False



