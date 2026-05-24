from django.contrib import admin
from .models import GalleryImage, GalleryCategory

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "hotel", "is_featured", "sort_order", "created_at")
    list_filter = ("category", "hotel", "is_featured")
    search_fields = ("title",)
    list_editable = ("is_featured", "sort_order")
