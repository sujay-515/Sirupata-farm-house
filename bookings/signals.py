from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking


@receiver(post_save, sender=Booking)
def send_booking_alert(sender, instance, created, **kwargs):
    if created:
        subject = "🛎️ New Booking Received - Sirupata R-Star"

        message = f"""
New booking received!

Name: {instance.name}
Email: {instance.email}
Phone: {instance.phone}

Room: {instance.room}
Check-in: {instance.check_in}
Check-out: {instance.check_out}
Guests: {instance.guests}

Booked on: {instance.created_at.strftime('%Y-%m-%d %H:%M')}
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # admin gmail
            fail_silently=False,
        )
