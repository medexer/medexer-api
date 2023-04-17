import uuid
from django.db import models


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class NotificationType(models.TextChoices):
    DONOR = "DONOR"
    HOSPITAL = "HOSPITAL"
        
class BloodGroup(models.TextChoices):
    OPositive = "O+"
    ONegative = "O-"
    ABPositive = "AB+"
    ABNegative = "AB-"
    APositive = "A+"
    ANegative = "A-"
    BPositive = "B+"
    BNegative = "B-"
        
class Genotype(models.TextChoices):
    AA = "AA"
    AS = "AS"
    AC = "AC"
    SS = "SS"
    SC = "SC"
        
class IdentificationType(models.TextChoices):
    VOTERCARD = "VOTERCARD"
    NATIONALIDENTITYCARD = "NATIONALIDENTITYCARD"
    CACCERTIFICATE = "CACCERTIFICATE"
        
class ComplaintStatusType(models.TextChoices):
    OPENED = "OPENED"
    CLOSED = "CLOSED"
    REOPENED = "REOPENED"
    IN_PROGRESS = "IN_PROGRESS"
