from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel, BloodGroup


class Inventory(TimeStampedUUIDModel):
    bloodGroup = models.CharField(max_length=255,blank=True, null=True)
    bloodUnits = models.PositiveIntegerField(default=0, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_hospitalID", blank=True, null=True, on_delete=models.CASCADE)
   

    def __str__(self):
        # return f"{self.hospital} - has {self.bloodUnits} of {self.bloodGroup}"
        return f"{self.hospital}"
    class Meta():
        verbose_name_plural = "Inventory"


class InventoryActivity(TimeStampedUUIDModel):
    activity = models.CharField(max_length=255, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_activity_hospitalID", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hospital} - {self.activity}"
    
    class Meta():
        verbose_name_plural = "Inventory Activities"