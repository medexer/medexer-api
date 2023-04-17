from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from apps.hospital.models import *


# @receiver(post_save, sender=Inventory)
# def create_(sender, instance, created, **kwargs): 
    
#     if not created:
#         result = InventoryActivity.objects.create(activity=instance.bloodUnits, hospitalID=instance.hospitalID, hospital=hospital)  
#         result.save()