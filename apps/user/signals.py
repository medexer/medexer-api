from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from apps.hospital.models import *
from apps.profile.models import Profile


@receiver(post_save, sender=User)
def create_(sender, instance, created, **kwargs):  
    items = ["O+","O-","AB+","AB-","A+","A-","B+","B-" ]  
    
    if created:
        if instance.is_hospital:
            hospital = User.objects.get(pk=instance.pkid) 
            for i in items:       
                inventory = Inventory.objects.create(bloodGroup=i,hospitalID=hospital.hospitalID,hospital=hospital)
                inventory.save()
                
            # intiialize hospital profile
            Profile.objects.create(
                user=hospital
            )
            
        # initialize user profile
        Profile.objects.create(
            user=instance
        )