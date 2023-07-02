from django.db import models
from apps.user.models import User
from apps.donor.models import Appointment
from apps.common.models import TimeStampedUUIDModel, BloodGroup, Genotype


class MedicalTest(TimeStampedUUIDModel):
    hiv = models.CharField(max_length=255, blank=True, null=True)
    hepatitisB = models.CharField(max_length=255, blank=True, null=True)
    hepatitisC = models.CharField(max_length=255, blank=True, null=True)
    vdrl = models.CharField(max_length=255, blank=True, null=True)
    bloodPressure = models.CharField(max_length=255, blank=True, null=True)
    bodyTemperature = models.CharField(max_length=255, blank=True, null=True)
    bloodGroup = models.CharField(max_length=255, choices=BloodGroup.choices, blank=True, null=True)
    genotype = models.CharField(max_length=255, choices=Genotype.choices, blank=True, null=True)
    pcv = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    appointment = models.ForeignKey(Appointment, related_name="medical_data_appointment", blank=True, null=True, on_delete=models.DO_NOTHING)
    donor = models.ForeignKey(User, related_name="medical_data_donor", blank=True, null=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, related_name="medical_data_author", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    class Meta:
        ordering = ('-pkid',)
        verbose_name_plural = "Medical Test"
        
    def __str__(self):
        return f"{self.donor}"
    