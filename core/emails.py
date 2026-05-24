from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def _sender_email():
    return getattr(settings, "DEFAULT_FROM_EMAIL", "") or settings.EMAIL_HOST_USER


def _send_booking_email(*, subject, template_name, booking):
    context = {
        "booking": booking,
        "site_name": settings.SITE_NAME,
        "site_url": settings.SITE_URL,
    }

    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=_sender_email(),
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception:
        return False


def send_booking_received_email(booking):
    subject = f"We received your booking request - {settings.SITE_NAME}"
    return _send_booking_email(
        subject=subject,
        template_name="emails/booking_received.html",
        booking=booking,
    )


def send_booking_confirmed_email(booking):
    subject = f"Your booking is confirmed - {settings.SITE_NAME}"
    return _send_booking_email(
        subject=subject,
        template_name="emails/booking_confirmed.html",
        booking=booking,
    )


def send_contact_submission_notification(submission):
    subject = f"Contact Form: {submission.subject}"
    message = (
        "New Contact Message\n\n"
        f"Name: {submission.name}\n"
        f"Email: {submission.email}\n\n"
        "Message:\n"
        f"{submission.message}"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=_sender_email(),
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
