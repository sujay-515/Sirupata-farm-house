from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image_file = models.ImageField(upload_to="rooms/", blank=True)
    image = models.CharField(max_length=255, blank=True)
    capacity = models.CharField(max_length=50, blank=True)
    amenities = models.TextField(blank=True, help_text="Enter one amenity per line or separate them with commas.")
    sort_order = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name

    @property
    def amenity_list(self):
        raw = (self.amenities or "").replace("\r", "\n")
        if "\n" in raw:
            parts = raw.split("\n")
        else:
            parts = raw.split(",")
        return [item.strip() for item in parts if item.strip()]
