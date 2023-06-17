from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "contact_number"]
