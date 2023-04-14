from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from apps.hospital.models import *


@receiver(post_save, sender=User)
def create_(sender, instance, created, **kwargs):  
    items = ["OPositive","ONegative","ABPositiv","ABNegativ","APositive","ANegative","BPositive","BNegative" ]  
    
    if created:
        if instance.is_hospital:
            hospital = User.objects.get(pk=instance.pkid) 
            for i in items:       
                inventory = Inventory.objects.create(bloodGroup=i,hospitalID=hospital.hospitalID,hospital=hospital)
                inventory.save()