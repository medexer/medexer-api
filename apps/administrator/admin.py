from django.contrib import admin
from .models import Notification, Complaint, ComplaintHistory, Integration


@admin.register(Integration)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "organization", "state", 'cac_id', 'is_approved']


@admin.register(Notification)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "notificationType", "author", 'recipient', 'is_read']


@admin.register(Complaint)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "title", "hospital"]


@admin.register(ComplaintHistory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "updateType", "headline"]
