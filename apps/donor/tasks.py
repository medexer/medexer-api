import os
from dotenv import load_dotenv
from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()

def send_contact_us_mail(donorEmail, subject, fullName, message):
    try:
        subject = f"{fullName}: {subject}"
        to = [os.getenv("EMAIL_HOST_USER")]
        from_email = os.getenv("EMAIL_HOST_USER")
        msg_html = render_to_string(
            "donor/contact_us_template.html",
            {
                "message": message,
                "donorName": fullName,
                "donorEmail": donorEmail,
            },
        )
        text_content = strip_tags(msg_html)

        mail = EmailMultiAlternatives(subject, text_content, from_email, to)
        mail.attach_alternative(msg_html, "text/html")
        mail.send()

        print(f"[SEND-CONTACT-US-MAIL-SUCCESS]")
        
        return True
    except Exception as e:
        print(f"[SEND-CONTACT-US-MAIL-ERROR] :: {e}")
        return False
