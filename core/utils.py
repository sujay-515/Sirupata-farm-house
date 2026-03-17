# core/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_review_notification(review):
    """
    Send email notification to admin when new review is submitted
    """
    subject = f'🔔 New Review Submitted - {review.user_name}'
    
    # Email context
    context = {
        'review': review,
        'admin_url': f"{settings.SITE_URL}/admin/core/review/{review.id}/change/",
        'site_name': 'Sirupata R Star'
    }
    
    try:
        # Render HTML email
        html_message = render_to_string('emails/new_review_notification.html', context)
        plain_message = strip_tags(html_message)  # Fallback for plain text
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_review_status_notification(review):
    """
    Send email to user when their review is approved/rejected
    """
    if not review.user_email:
        return False
    
    if review.status == 'approved':
        subject = f'✅ Your Review at {settings.SITE_NAME} has been Approved!'
        template = 'emails/review_approved.html'
    elif review.status == 'rejected':
        subject = f'📝 Update on Your Review at {settings.SITE_NAME}'
        template = 'emails/review_rejected.html'
    else:
        return False
    
    context = {
        'review': review,
        'site_name': 'Sirupata R Star'
    }
    
    try:
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[review.user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False# core/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_review_notification(review):
    """
    Send email notification to admin when new review is submitted
    """
    subject = f'🔔 New Review Submitted - {review.user_name}'
    
    # Email context
    context = {
        'review': review,
        'admin_url': f"{settings.SITE_URL}/admin/core/review/{review.id}/change/",
        'site_name': 'Sirupata R Star'
    }
    
    try:
        # Render HTML email
        html_message = render_to_string('emails/new_review_notification.html', context)
        plain_message = strip_tags(html_message)  # Fallback for plain text
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_review_status_notification(review):
    """
    Send email to user when their review is approved/rejected
    """
    if not review.user_email:
        return False
    
    if review.status == 'approved':
        subject = f'✅ Your Review at {settings.SITE_NAME} has been Approved!'
        template = 'emails/review_approved.html'
    elif review.status == 'rejected':
        subject = f'📝 Update on Your Review at {settings.SITE_NAME}'
        template = 'emails/review_rejected.html'
    else:
        return False
    
    context = {
        'review': review,
        'site_name': 'Sirupata R Star'
    }
    
    try:
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[review.user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False