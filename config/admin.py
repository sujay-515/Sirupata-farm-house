from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from core.models import Booking, Review
from bookings.models import Booking as BookingModel  # if different
from django.utils import timezone
from datetime import timedelta
import json

class CustomAdminSite(AdminSite):
    site_header = "Sirupata Farm House Admin"
    site_title = "Admin Portal"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Stats
        extra_context['total_bookings'] = Booking.objects.count()
        extra_context['total_reviews'] = Review.objects.count()
        extra_context['pending_reviews'] = Review.objects.filter(status='pending').count()
        now = timezone.now()
        start_of_month = now.replace(day=1)
        extra_context['recent_bookings'] = Booking.objects.filter(created_at__gte=start_of_month).count()

        # Recent bookings
        extra_context['recent_bookings_list'] = Booking.objects.order_by('-created_at')[:5]

        # Chart data: bookings per month for last 12 months
        months = []
        data = []
        for i in range(11, -1, -1):
            month_start = (now - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            count = Booking.objects.filter(created_at__gte=month_start, created_at__lte=month_end).count()
            months.append(month_start.strftime('%b %Y'))
            data.append(count)
        extra_context['bookings_chart_data'] = json.dumps({'labels': months, 'data': data})

        return super().index(request, extra_context)

# Instantiate the custom admin site
admin_site = CustomAdminSite(name='admin')

# Make it the default admin site
admin.site = admin_site