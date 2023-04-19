from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel, NotificationType, ComplaintStatusType


class Notification(TimeStampedUUIDModel):
    notificationType = models.CharField(max_length=255, choices=NotificationType.choices, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, related_name="notification_author", blank=True, null=True, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="notification_recipient", blank=True, null=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notificationType} - {self.message}"
    
    class Meta:
        ordering = ('-pkid',)
    
    
class Complaint(TimeStampedUUIDModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=ComplaintStatusType.choices, blank=True, null=True)
    complaintID = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # message = models.TextField(blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="complaint_hospital", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    class Meta:
        ordering = ('-pkid',)
    
    def __str__(self):
        return f"{self.hospitalID} - {self.title}"
    
    
class ComplaintHistory(TimeStampedUUIDModel):
    updateType = models.CharField(max_length=255, default="THREAD", blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    complaint = models.ForeignKey(Complaint, related_name="complaint", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.complaint.hospital.hospitalName} - {self.complaint}"

    class Meta():
        verbose_name_plural = "Complaint History"