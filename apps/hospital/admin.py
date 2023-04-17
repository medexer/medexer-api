from django.contrib import admin
from .models import Inventory, InventoryActivity


@admin.register(Inventory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "bloodGroup", "bloodUnits", "hospital"]


@admin.register(InventoryActivity)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "hospital", "activity"]
