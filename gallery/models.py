from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)

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
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="gallery/")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Image {self.id}"
