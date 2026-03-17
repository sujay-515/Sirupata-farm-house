from django.contrib import admin
from .models import GalleryImage, GalleryCategory

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "created_at")
    list_filter = ("category", "is_featured")
    search_fields = ("title",)
