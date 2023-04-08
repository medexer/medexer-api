from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel


class Appointment(TimeStampedUUIDModel):
    date = models.DateField(blank=True, null=True)    
    donor = models.ForeignKey(User, related_name="appointment_donorID", blank=True, null=True, on_delete=models.DO_NOTHING)
    hospital = models.ForeignKey(User, related_name="appointment_hospitalID", blank=True, null=True, on_delete=models.DO_NOTHING)
    message = models.TextField()
    
    def __str__(self):
        return f"{self.donor} - {self.hospital} {self.date}"