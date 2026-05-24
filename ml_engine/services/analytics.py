from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.utils import timezone

from core.models import Booking

MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def get_active_booking_filter():
    return ~Q(status="cancelled")


def get_room_popularity_map():
    counts = Booking.objects.values("room").annotate(count=Count("id"))
    return {item["room"]: item["count"] for item in counts}


def get_operations_snapshot(*, today=None, recent_limit=5, upcoming_limit=6):
    today = today or timezone.localdate()
    active_filter = get_active_booking_filter()

    today_checkins = Booking.objects.filter(active_filter, checkin=today).order_by("checkin", "created_at")[:recent_limit]
    today_checkouts = Booking.objects.filter(active_filter, checkout=today).order_by("checkout", "created_at")[:recent_limit]
    upcoming_bookings = Booking.objects.filter(
        active_filter,
        checkin__gte=today,
    ).order_by("checkin", "created_at")[:upcoming_limit]

    return {
        "today": today,
        "today_checkins_count": Booking.objects.filter(active_filter, checkin=today).count(),
        "today_checkouts_count": Booking.objects.filter(active_filter, checkout=today).count(),
        "today_checkins": today_checkins,
        "today_checkouts": today_checkouts,
        "upcoming_bookings": upcoming_bookings,
        "recent_bookings_list": Booking.objects.filter(active_filter).order_by("-created_at")[:recent_limit],
    }


def get_booking_trend_data(*, period=12, now=None):
    now = now or timezone.now()
    labels = []
    data = []
    for i in range(period - 1, -1, -1):
        month_start = (now - timedelta(days=30 * i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        labels.append(month_start.strftime("%b %Y"))
        data.append(
            Booking.objects.filter(created_at__gte=month_start, created_at__lte=month_end).count()
        )
    return {"labels": labels, "data": data}


def get_room_booking_breakdown(*, top_n=8):
    active_filter = get_active_booking_filter()
    room_stats = list(
        Booking.objects.filter(active_filter)
        .values("room")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    top_rooms = room_stats[:top_n]
    other_total = sum(item["total"] for item in room_stats[top_n:])
    labels = [item["room"] for item in top_rooms]
    data = [item["total"] for item in top_rooms]

    if other_total > 0:
        labels.append("Other")
        data.append(other_total)

    return {
        "labels": labels,
        "data": data,
        "top_rooms": top_rooms,
    }


def get_top_rooms(*, limit=5, top_n=8):
    breakdown = get_room_booking_breakdown(top_n=top_n)
    return [{"room": item["room"], "total": item["total"]} for item in breakdown["top_rooms"][:limit]]


def get_stay_month_trend_data():
    active_filter = get_active_booking_filter()
    monthly_counts = {index: 0 for index in range(1, 13)}

    queryset = (
        Booking.objects.filter(active_filter)
        .annotate(month=ExtractMonth("checkin"))
        .values("month")
        .annotate(total=Count("id"))
    )

    for item in queryset:
        month = item["month"]
        if month:
            monthly_counts[month] = item["total"]

    data = [monthly_counts[index] for index in range(1, 13)]
    max_count = max(data) if data else 0
    points = [
        {
            "index": index,
            "label": MONTH_LABELS[index - 1],
            "count": monthly_counts[index],
            "height_percent": int((monthly_counts[index] / max_count) * 100) if max_count else 0,
        }
        for index in range(1, 13)
    ]
    ranked_months = [
        {"index": index, "label": MONTH_LABELS[index - 1], "count": monthly_counts[index]}
        for index in range(1, 13)
    ]
    ranked_months.sort(key=lambda item: item["count"], reverse=True)

    nonzero_months = [item for item in ranked_months if item["count"] > 0]
    peak_months = nonzero_months[:3]
    quieter_months = list(reversed(nonzero_months[-2:])) if nonzero_months else []

    return {
        "labels": MONTH_LABELS,
        "data": data,
        "points": points,
        "peak_months": peak_months,
        "quieter_months": quieter_months,
        "peak_month_label": peak_months[0]["label"] if peak_months else None,
        "total_stays": sum(data),
    }
