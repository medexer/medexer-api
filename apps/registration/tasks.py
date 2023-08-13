import os
from dotenv import load_dotenv
from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()

def send_hospital_complaince_mail(target_mail, hospitalName):
    try:
        subject = f"Medexer"
        to = [target_mail]
        from_email = os.getenv("EMAIL_HOST_USER")
        msg_html = render_to_string(
            "registration/hospital_compliance_template.html",
            {
                "hospitalName": hospitalName,
            },
        )
        text_content = strip_tags(msg_html)

        mail = EmailMultiAlternatives(subject, text_content, from_email, to)
        mail.attach_alternative(msg_html, "text/html")
        mail.send()

        print(f"[SEND-COMPLAINCE-MAIL-SUCCESS]")
    except Exception as e:
        print(f"[SEND-COMPLAINCE-MAIL-ERROR] :: {e}")