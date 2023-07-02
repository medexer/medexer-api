from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from apps.hospital.models import *
from apps.profile.models import Profile


@receiver(post_save, sender=User)
def create_(sender, instance, created, **kwargs):  
    bloodGroups = ["O+","O-","AB+","AB-","A+","A-","B+","B-" ]  
    
    if created:
        if instance.is_hospital:
            hospital = User.objects.get(pk=instance.pkid) 
            
            for bloodGroup in bloodGroups:       
                Inventory.objects.create(
                    bloodGroup=bloodGroup,
                    hospital=hospital,
                    hospitalID=hospital.hospitalID,
                )
                
            # intiialize hospital profile
            return Profile.objects.create(
                user=hospital,
                address=instance.address,
                state=instance.state,
                city_province=instance.lga,
            )

        # else:
        #     return Profile.objects.create(
        #         user=instance
        #     )