from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from apps.administrator.models import *


@receiver(post_save, sender=Appointment)
def create_notification(sender, instance, created, **kwargs):    
    if created:
        notification = Notification.objects.create(
            title="Appointment",
            notificationType='APPOINTMENT',
            recipient=instance.donor,
            author=instance.hospital,
            message=f'You have scheduled a new appointment with {instance.hospital.hospitalName} for {instance.date}',
        )
        notification.save()
    
        hospitalNotification = Notification.objects.create(
            title="Appointment",
            author=instance.donor,
            recipient=instance.hospital,
            notificationType='APPOINTMENT',
            message=f'You have a new appointment scheduled with {instance.donor.fullName} on the {instance.date}',
        )
        hospitalNotification.save()
  