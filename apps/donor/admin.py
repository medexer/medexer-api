from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "hospital", "date"]