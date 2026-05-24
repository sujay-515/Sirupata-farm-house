from django.db import models, transaction

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name="images"
    )
    hotel = models.ForeignKey(
        "core.Hotel",
        on_delete=models.CASCADE,
        related_name="gallery_images",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="gallery/")
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "sort_order", "-created_at"]

    def __str__(self):
        return self.title or f"Image {self.id}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.is_featured and self.hotel_id:
                (
                    GalleryImage.objects.filter(hotel_id=self.hotel_id, is_featured=True)
                    .exclude(pk=self.pk)
                    .update(is_featured=False)
                )
