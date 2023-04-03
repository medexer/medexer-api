from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel


class Appointment(TimeStampedUUIDModel):
    date = models.DateField(blank=True, null=True)
    donorID = models.CharField(max_length=255, blank=True, null=True)
    donor = models.ForeignKey(User, related_name="appointment_donorID", blank=True, null=True, on_delete=models.DO_NOTHING)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="appointment_hospitalID", blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.donorID} - {self.hospital} {self.date}"