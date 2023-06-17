from django.contrib import admin
from .models import Notification, Complaint, ComplaintHistory, Integration, PaymentHistory


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
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


@admin.register(PaymentHistory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "amount_paid", "hospital"]
