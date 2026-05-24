import json

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.utils import timezone

from core.models import Booking, Review
from core.models import SiteContent
from ml_engine.services.analytics import (
    get_active_booking_filter,
    get_booking_trend_data,
    get_operations_snapshot,
    get_room_booking_breakdown,
    get_stay_month_trend_data,
    get_top_rooms,
)


class CustomAdminSite(AdminSite):
    site_header = "Sirupata Farm House Admin"
    site_title = "Admin Portal"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Period choice for charting (defaults to 12 months)
        period_months = request.GET.get('period', '12')
        if period_months not in ['3', '6', '12']:
            period_months = '12'
        period = int(period_months)
        extra_context['period'] = period

        # Stats
        extra_context['total_bookings'] = Booking.objects.count()
        extra_context['total_reviews'] = Review.objects.count()
        extra_context['pending_reviews'] = Review.objects.filter(status='pending').count()

        now = timezone.now()
        today = timezone.localdate()
        start_of_month = now.replace(day=1)
        active_booking_filter = get_active_booking_filter()
        extra_context['recent_bookings'] = Booking.objects.filter(active_booking_filter, created_at__gte=start_of_month).count()
        extra_context.update(get_operations_snapshot(today=today))

        # quick admin action links
        extra_context['pending_reviews_url'] = reverse('admin:core_review_changelist') + '?status__exact=pending'
        extra_context['create_booking_url'] = reverse('admin:core_booking_add')
        extra_context['all_bookings_url'] = reverse('admin:core_booking_changelist')
        extra_context['all_reviews_url'] = reverse('admin:core_review_changelist')
        content_obj = SiteContent.objects.order_by("id").first()
        extra_context['site_content_url'] = reverse('admin:core_sitecontent_changelist')
        if content_obj:
            extra_context['site_content_url'] = reverse('admin:core_sitecontent_change', args=[content_obj.pk])
        extra_context['about_locations_url'] = reverse('admin:core_aboutlocation_changelist')
        extra_context['today_checkins_url'] = f"{extra_context['all_bookings_url']}?checkin__exact={today.isoformat()}"
        extra_context['today_checkouts_url'] = f"{extra_context['all_bookings_url']}?checkout__exact={today.isoformat()}"

        # Latest recent reviews for sidebar
        extra_context['latest_reviews'] = Review.objects.order_by('-created_at')[:5]

        extra_context['bookings_chart_data'] = json.dumps(get_booking_trend_data(period=period, now=now))
        stay_trend = get_stay_month_trend_data()
        extra_context['stay_month_chart_data'] = json.dumps({
            'labels': stay_trend['labels'],
            'data': stay_trend['data'],
        })
        extra_context['peak_stay_months'] = stay_trend['peak_months']
        extra_context['quieter_stay_months'] = stay_trend['quieter_months']
        room_breakdown = get_room_booking_breakdown(top_n=8)
        extra_context['room_bookings_chart_data'] = json.dumps({
            'labels': room_breakdown['labels'],
            'data': room_breakdown['data'],
        })
        extra_context['top_rooms'] = get_top_rooms(limit=5, top_n=8)

        return super().index(request, extra_context)

default_admin_site = admin.site

# Instantiate the custom admin site and preserve everything already discovered
# by Django's admin autodiscovery, including auth and app-specific models.
admin_site = CustomAdminSite(name='admin')
for model, model_admin in default_admin_site._registry.items():
    admin_site.register(model, model_admin.__class__)

# Make it the default admin site used by urls.
admin.site = admin_site
