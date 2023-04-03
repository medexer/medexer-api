import uuid
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fullName = models.CharField(verbose_name=_("Full Name"), max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True, blank=True, null=True)
    location = models.EmailField(verbose_name=_("Location"), blank=True, null=True)
    hospitalName = models.EmailField(verbose_name=_("Hospital Name"), blank=True, null=True)
    donorID = models.EmailField(verbose_name=_("Donor ID"), unique=True, blank=True, null=True)
    hospitalID = models.EmailField(verbose_name=_("Hospital ID"), unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_donor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    otp = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    is_kyc_updated = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullName"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        if self.fullName:
            return f"{self.fullName}"
        if self.hospitalName:
            return f"{self.hospitalName}"
