from django.contrib import admin
from .models import Notification, Complaint, ComplaintHistory


@admin.register(Notification)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "notificationType", "author", 'recipient']


@admin.register(Complaint)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "title", "hospital"]


@admin.register(ComplaintHistory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "updateType", "headline"]
