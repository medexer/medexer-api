from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel


class Appointment(TimeStampedUUIDModel):
    date = models.DateField(blank=True, null=True)    
    donor = models.ForeignKey(User, related_name="appointment_donor", blank=True, null=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(User, related_name="appointment_hospital", blank=True, null=True, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    pints = models.CharField(max_length=255, default="0", blank=True, null=True)
    donationDate = models.DateField(blank=True, null=True)
    isDonated = models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self):
        return f"{self.donor} - {self.hospital} {self.date}"
    
    class Meta:
        ordering = ('-pkid',)

class DonationHistory(TimeStampedUUIDModel):
    donor = models.ForeignKey(User, related_name="donation_history_donor", blank=True, null=True, on_delete=models.DO_NOTHING)
    # appointment = models.ForeignKey(Appointment, related_name="appointment_activity", blank=True, null=True, on_delete=models.DO_NOTHING)
    message = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = ('Donation History')
    
    def __str__(self):
        return f"{self.donor} - {self.message}"
    