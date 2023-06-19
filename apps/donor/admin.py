from django.contrib import admin
from .models import Appointment, DonationHistory


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "appointmentID", "donor", "hospital", "date"]

@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "message"]