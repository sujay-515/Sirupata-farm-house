from django.shortcuts import render
from .models import GalleryCategory

def gallery(request):
    categories = []
    for category in GalleryCategory.objects.prefetch_related("images"):
        images = list(category.images.all())
        if not images:
            continue

        featured_images = [image for image in images if image.is_featured]
        lead_image = featured_images[0] if featured_images else images[0]
        supporting_images = [image for image in images if image.pk != lead_image.pk][:6]
        categories.append({
                "category": category,
                "lead_image": lead_image,
                "supporting_images": supporting_images,
                "image_count": len(images),
            })

    return render(request, "gallery/gallery.html", {
        "categories": categories,
    })
