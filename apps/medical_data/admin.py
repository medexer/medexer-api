from django.contrib import admin
from .models import MedicalTest


@admin.register(MedicalTest)
class MedicalTestAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "donor", "hiv"]
