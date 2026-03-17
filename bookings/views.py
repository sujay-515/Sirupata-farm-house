from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import Booking

def booking_form(request):
    if request.method == "POST":
        booking = Booking(
            checkin=request.POST.get("checkin"),
            checkout=request.POST.get("checkout"),
            guests=request.POST.get("guests"),
            room=request.POST.get("room"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
        )

        try:
            booking.full_clean()
            booking.save()
            return render(request, "bookings/booking_form.html", {
                "success": True
            })

        except ValidationError as e:
            return render(request, "bookings/booking_form.html", {
                "errors": e.messages
            })

    return render(request, "bookings/booking_form.html")
