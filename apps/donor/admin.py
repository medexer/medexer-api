from django.contrib import admin
from .models import Appointment, DonationHistory


@admin.register(Appointment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "hospital", "date"]

@admin.register(DonationHistory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "message"]