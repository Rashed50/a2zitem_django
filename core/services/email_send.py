from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime
import requests

def html_mail_sender(subject, html_content, to, from_email=None, cc=None, bcc=None):
    try:
        if not from_email:
            from_email = f"ABC Ltd <{settings.EMAIL_HOST_USER}>"

        ##? Ensure 'to' is always a list
        if isinstance(to, str):
            to = [to]

        ##? Ensure 'cc' is always a list
        if cc and isinstance(cc, str):
            cc = [cc]
            
        ##? Ensure 'bcc' is always a list
        if bcc and isinstance(bcc, str):
            bcc = [bcc]
        
        ##? List Concatenation
        # to  = [to] if isinstance(to, str) else to
        # cc  = [cc] if isinstance(cc, str) else (cc or [])
        # bcc = [bcc] if isinstance(bcc, str) else (bcc or [])

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject    = subject,
            body       = text_content,
            from_email = from_email,
            to         = to,
            cc         = cc,
            bcc        = bcc
        )
        email.attach_alternative(html_content, "text/html")
        return email.send()
    except Exception as e:
        print("-----------------------------")
        print("Email send error:", e)
        print("-----------------------------")
        return None
 
 
# def send_restricted_item_email(instance, to_email, cc_emails=None, bcc_emails=None):
#     from django.template.loader import render_to_string
#     try:
#         subject = "E-Challan Notification"

#         chalan_items = instance.chalan.all()

#         html_content = render_to_string('dashboard/email/echallan/restricted_item_notification.html', {
#             "chalan": instance,
#             "user"  : instance.signature_hof,
#             "chalan_items": chalan_items,
#         })

#         return html_mail_sender(
#             subject      = subject,           ## Subject
#             html_content = html_content,      ## Body
#             from_email   = None,              ## settings.py DEFAULT_FROM_EMAIL use হবে
#             to           = to_email,          ## এখন list দিতে পারবেন
#             cc           = cc_emails or [],   ## optional CC list
#             bcc          = bcc_emails or []   ## optional BCC list
#         )
#     except Exception as e:
#         print("-----------------------------")
#         print("Error in send_restricted_item_email:")
#         print(e)
#         print("-----------------------------")
#         return 0
 
 
    

