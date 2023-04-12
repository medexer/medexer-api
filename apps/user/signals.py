from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from apps.hospital.models import *


@receiver(post_save, sender=User)
def create_(sender, instance, created, **kwargs):    
    if created:
        if instance.is_hospital:
            hospital = User.objects.get(pk=instance.pkid)        
            inventory = Inventory.objects.create(hospitalID=hospital.hospitalID,hospital=hospital)
            inventory.save()