from django.db import models
from apps.user.models import User
from apps.common.models import TimeStampedUUIDModel
from apps.common.models import BloodGroup, Genotype
from apps.common.media import hospital_image_path, avatar_path


class Profile(TimeStampedUUIDModel):
    dateOfBirth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    about_hospital = models.TextField(blank=True, null=True)
    city_province = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=255, blank=True, null=True)
    bloodGroup = models.CharField(max_length=255, choices=BloodGroup.choices, blank=True, null=True)
    genotype = models.CharField(max_length=255, choices=Genotype.choices, blank=True, null=True)
    userAvatar = models.ImageField(upload_to=avatar_path, default="/images/profile/avatar__1.png", blank=True, null=True)
    is_profile_updated = models.BooleanField(default=False)
    hospitalImage = models.ImageField(upload_to=hospital_image_path, default="/images/profile/hospital__1.jpg", blank=True, null=True)
    user = models.ForeignKey(User, related_name="profile_user", blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Profile"
        
    def __str__(self):
        return f"{self.user}"