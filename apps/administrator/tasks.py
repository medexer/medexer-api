import os
from dotenv import load_dotenv
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()

def send_integration_request_mail(target_mail, accessKey):
    try:
        subject = "Medexer: Integration Request"
        to = [target_mail]
        from_email = os.getenv("EMAIL_HOST_USER")
        msg_html = render_to_string(
            "administrator/approve_integration_request.html",
            {
                "email": target_mail,
                "accessKey": accessKey,
            },
        )
        text_content = strip_tags(msg_html)

        mail = EmailMultiAlternatives(subject, text_content, from_email, to)
        mail.attach_alternative(msg_html, "text/html")
        mail.send()

        print(f"[SEND-MAIL-SUCCESS]")
    except Exception as e:
        print(f"[SEND-MAIL-ERROR] :: {e}")
