from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from apps.administrator.models import *


# make sure you register signal file in app.py file

@receiver(post_save, sender=Appointment)
def create_notification(sender, instance, created, **kwargs):

    if not created:
        user_data = User.objects.get(fullName=instance.donor)
        notification = Notification.objects.create(author=instance.donor,
        message=instance.message + " " + str(instance.date),
        userID=user_data.id,notificationType='DONOR',hospitalID=instance.hospital)
        notification.save()

    user_details = User.objects.get(fullName=instance.donor)
    notification = Notification.objects.create(author=user_details,
    message=instance.message,
    userID=user_details.id,notificationType='HOSPITAL',hospitalID=instance.hospital)
    notification.save()

  