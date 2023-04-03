from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel, NotificationType


class Notification(TimeStampedUUIDModel):
    message = models.CharField(max_length=255, blank=True, null=True)
    notificationType = models.CharField(max_length=255, choices=NotificationType.choices, blank=True, null=True)
    userID = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, related_name="notification_author", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.notificationType} - {self.message[0:10]}"

    
    
class Complaint(TimeStampedUUIDModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="complaint_hospital", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.hospitalID} - {self.title}"
    
    
class ComplaintHistory(TimeStampedUUIDModel):
    headline = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    complaint = models.ForeignKey(Complaint, related_name="complaint", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.headline} - {self.title}"

    class Meta():
        verbose_name_plural = "Complaint History"