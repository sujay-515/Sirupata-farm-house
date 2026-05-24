from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "capacity", "is_available", "sort_order")
    list_filter = ("is_available",)
    search_fields = ("name", "description", "amenities")
    ordering = ("sort_order", "name")
