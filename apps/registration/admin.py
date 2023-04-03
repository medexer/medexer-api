from django.contrib import admin
from .models import KnowYourCustomer, KnowYourBusiness


@admin.register(KnowYourCustomer)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "bloodGroup", "documentUploadCover"]



@admin.register(KnowYourBusiness)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "hospital", "documentUploadCover"]

