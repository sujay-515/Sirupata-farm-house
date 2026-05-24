from django.db import models
from django.core.exceptions import ValidationError
import datetime

# Legacy model kept for migration compatibility.
# The live public booking flow now uses core.models.Booking.
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    room = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_in < datetime.date.today():
            raise ValidationError("Check-in date cannot be in the past.")
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

    def __str__(self):
        return f"{self.name} - {self.room}"
