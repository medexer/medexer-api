import os
from dotenv import load_dotenv
from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()

# @shared_task(bind=True)
# def send_forgotpassword_mail(self, target_mail, token):


def send_hospital_welcome_mail(target_mail, hospitalName, hospitalID):
    try:
        subject = f"Medexer"
        to = [target_mail]
        from_email = os.getenv("EMAIL_HOST_USER")
        msg_html = render_to_string(
            "user/hospital_welcome_template.html",
            {
                "email": target_mail,
                "hospitalID": hospitalID,
                "hospitalName": hospitalName,
            },
        )
        text_content = strip_tags(msg_html)

        mail = EmailMultiAlternatives(subject, text_content, from_email, to)
        mail.attach_alternative(msg_html, "text/html")
        mail.send()

        print(f"[SEND-MAIL-SUCCESS]")
    except Exception as e:
        print(f"[SEND-MAIL-ERROR] :: {e}")


def send_forgotpassword_mail(target_mail, token):
    try:
        # mail_subject = "Welcome on Board!"
        # send_mail(
        #     subject = mail_subject,
        #     message=message,
        #     from_email=os.getenv("EMAIL_HOST_USER"),
        #     recipient_list=[target_mail],
        #     fail_silently=False,
        #     )

        subject = f"Medexer: Forgot Password OTP"
        to = [target_mail]
        from_email = os.getenv("EMAIL_HOST_USER")
        msg_html = render_to_string(
            "user/forgotpassword.html",
            {"token": token},
        )
        text_content = strip_tags(msg_html)

        mail = EmailMultiAlternatives(subject, text_content, from_email, to)
        mail.attach_alternative(msg_html, "text/html")
        mail.send()

        print(f"[SEND-MAIL-SUCCESS]")
    except Exception as e:
        print(f"[SEND-MAIL-ERROR] :: {e}")
