from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    room = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.room}"
