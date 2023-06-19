from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel, BloodGroup


class Inventory(TimeStampedUUIDModel):
    bloodGroup = models.CharField(max_length=255,blank=True, null=True)
    bloodUnits = models.PositiveIntegerField(default=0, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_hospitalID", blank=True, null=True, on_delete=models.CASCADE)
   
    def __str__(self):
        return f"{self.hospital}"      
              
    class Meta():
        verbose_name_plural = "Inventory"


class InventoryItem(TimeStampedUUIDModel):
    bloodGroup = models.CharField(max_length=255,blank=True, null=True)
    bloodUnits = models.PositiveIntegerField(default=0, blank=True, null=True)
    appointmentID = models.CharField(max_length=255, null=True, blank=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    donor = models.ForeignKey(User, related_name="inventory_item_donor", blank=True, null=True, on_delete=models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, related_name="inventoryitem_inventory", blank=True, null=True, on_delete=models.CASCADE)
   
    def __str__(self):
        return f"{self.bloodGroup} - {self.bloodUnits}" 
                   
    class Meta():
        verbose_name_plural = "Inventory Item"


class InventoryActivity(TimeStampedUUIDModel):
    activity = models.TextField(blank=True, null=True)
    bloodGroup = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_activity_hospitalID", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hospital} - {self.activity}"
    
    class Meta():
        ordering = ("-pkid",)
        verbose_name_plural = "Inventory Activity"