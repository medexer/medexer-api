from django.db import models
from apps.user.models import User
from apps.common.media import kyc_document_path, kyb_document_path
from apps.common.models import TimeStampedUUIDModel, BloodGroup, Genotype, IdentificationType


class KnowYourCustomer(TimeStampedUUIDModel):
    bloodGroup = models.CharField(max_length=255, choices=BloodGroup.choices, blank=True, null=True)
    genotype = models.CharField(max_length=255, choices=Genotype.choices, blank=True, null=True)
    haveDonatedBlood = models.BooleanField(default=False)
    lastBloodDonationTime = models.CharField(max_length=255, blank=True, null=True)
    tobaccoUsage = models.BooleanField(default=False)
    isRecentVaccineRecipient = models.BooleanField(default=False)
    hasTattos = models.BooleanField(default=False)
    identificationType = models.CharField(max_length=255, choices=IdentificationType.choices, blank=True, null=True)
    documentUploadCover =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    documentUploadRear =models.ImageField(upload_to=kyc_document_path, blank=True, null=True)
    donorID = models.CharField(max_length=255, blank=True, null=True)
    donor = models.ForeignKey(User, related_name="kyc_donor", blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.donor} KYC"



class KnowYourBusiness(TimeStampedUUIDModel):
    cacRegistrationID = models.CharField(max_length=255, blank=True, null=True)
    websiteUrl = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to=kyb_document_path, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    incorporation_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    identificationType = models.CharField(max_length=255, choices=IdentificationType.choices, default="CACCERTIFICATE", blank=True, null=True)
    hospitalID = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.ForeignKey(User, related_name="kyb_hospital", blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.hospital} KYB"
    
    class Meta():
        verbose_name_plural = "Know Your Businesses"
