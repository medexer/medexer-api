from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel, BloodGroup


class Inventory(TimeStampedUUIDModel):
    # bloodGroup = models.CharField(max_length=255, choices=BloodGroup.choices, blank=True, null=True)
    # bloodUnits = models.PositiveIntegerField(default=0, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_hospitalID", blank=True, null=True, on_delete=models.DO_NOTHING)
    OPositive = models.PositiveIntegerField(default=0, blank=True, null=True)
    ONegative = models.PositiveIntegerField(default=0, blank=True, null=True)
    ABPositive = models.PositiveIntegerField(default=0, blank=True, null=True)
    ABNegative = models.PositiveIntegerField(default=0, blank=True, null=True)
    APositive = models.PositiveIntegerField(default=0, blank=True, null=True)
    ANegative = models.PositiveIntegerField(default=0, blank=True, null=True)
    BPositive = models.PositiveIntegerField(default=0, blank=True, null=True)
    BNegative = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        # return f"{self.hospital} - has {self.bloodUnits} of {self.bloodGroup}"
        return f"{self.hospital}"
    class Meta():
        verbose_name_plural = "Inventory"


class InventoryActivity(TimeStampedUUIDModel):
    activity = models.CharField(max_length=255, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="inventory_activity_hospitalID", blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.hospital} - {self.activity}"
    
    class Meta():
        verbose_name_plural = "Inventory Activities"