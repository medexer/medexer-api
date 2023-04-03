from django.db import models
from apps.user.models import User
from apps.common.media import kyc_document_path
from apps.common.models import TimeStampedUUIDModel, BloodGroup, Genotype, IdentificationType


class KnowYourCustomer(TimeStampedUUIDModel):
    bloodGroup = models.CharField(max_length=255, choices=BloodGroup.choices, blank=True, null=True)
    genotype = models.CharField(max_length=255, choices=Genotype.choices, blank=True, null=True)
    haveDonatedBlood = models.BooleanField(default=False)
    lastBloodDonationTime = models.CharField(max_length=255, blank=True, null=True)
    hasTattos = models.BooleanField(default=False)
    identificationType = models.CharField(max_length=255, choices=IdentificationType.choices, blank=True, null=True)
    documentUploadCover =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    documentUploadRear =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    donorID = models.CharField(max_length=255, blank=True, null=True)
    donor = models.ForeignKey(User, related_name="kyc_donor", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.donor} KYC"



class KnowYourBusiness(TimeStampedUUIDModel):
    identificationType = models.CharField(max_length=255, choices=IdentificationType.choices, blank=True, null=True)
    documentUploadCover =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    documentUploadRear =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="kyb_hospital", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.hospital} KYB"
    
    class Meta():
        verbose_name_plural = "Know Your Businesses"