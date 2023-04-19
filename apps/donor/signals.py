from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from apps.administrator.models import *


@receiver(post_save, sender=Appointment)
def create_appointment_notification(sender, instance, created, **kwargs):    
    if created:
        notification = Notification.objects.create(
            title="New appointment request.",
            notificationType='APPOINTMENT',
            recipient=instance.donor,
            author=instance.hospital,
            message=f'You have requested for a new appointment with {instance.hospital.hospitalName}. A date will be scheduled by the hospital and you will get a response.',
        )
        notification.save()
    
        hospitalNotification = Notification.objects.create(
            title=f"New appointment request.",
            author=instance.donor,
            recipient=instance.hospital,
            notificationType='APPOINTMENT',
            message=f'You have a new appointment request from {instance.donor.fullName}. Please schedule a date to alert them.',
        )
        hospitalNotification.save()
  