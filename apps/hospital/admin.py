from django.contrib import admin
from .models import Inventory, InventoryActivity, InventoryItem


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "bloodGroup", "bloodUnits", "hospital"]


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "bloodGroup", "bloodUnits"]


@admin.register(InventoryActivity)
class InventoryActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "hospital", "activity"]
