from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from apps.administrator.models import *


@receiver(post_save, sender=Appointment)
def create_notification(sender, instance, created, **kwargs):    
    if created:
        notification = Notification.objects.create(
            notificationType='DONOR',
            recipient=instance.donor,
            author=instance.hospital,
            message=instance.message + " " + str(instance.date),
        )
        notification.save()
    
        hospitalNotification = Notification.objects.create(
            notificationType='HOSPITAL',
            author=instance.donor,
            recipient=instance.hospital,
            message=instance.message + " " + str(instance.date),
        )
        hospitalNotification.save()
  