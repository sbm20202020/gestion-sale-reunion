from django.contrib import admin

from .models import Equipment, Room


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "location", "is_active")
    list_filter = ("is_active",)
    filter_horizontal = ("equipments",)
