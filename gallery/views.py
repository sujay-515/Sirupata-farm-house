from django.shortcuts import render
from .models import GalleryCategory

def gallery(request):
    categories = GalleryCategory.objects.prefetch_related("images")
    return render(request, "gallery/gallery.html", {
        "categories": categories
    })
