from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Movie, Screening, ScreeningSeat, Booking, BookingDetail
from collections import defaultdict
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


def start(request):
    return render(request, "booking/start_project.html")

def movie_list(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, "booking/movies.html", context)

def seat_selector(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    screening_seats = ScreeningSeat.objects.filter(screening=screening).select_related("seat").order_by("seat__row_letter", "seat__column_number")

    seats_by_row = defaultdict(list)

    for ss in screening_seats:
        seats_by_row[ss.seat.row_letter].append(ss)

    context = {
        "screening": screening,
        "seats_by_row": dict(seats_by_row)
    }
    
    return render(request, "booking/seat_selector.html", context)

def purchase_seats(request, pk):
    booking_details = BookingDetail.objects.filter(booking=pk).select_related("screening_seat").order_by("screening_seat__seat__row_letter", "screening_seat__seat__column_number")
    booking_detail = BookingDetail.objects.get(booking=pk)
    screening = get_object_or_404(Screening, pk=booking_detail.screening_seat.screening.id)
    total_price_paid = 0

    for detail in booking_details:
        total_price_paid += detail.price_paid_cents
    
    total_price_paid /= 100

    context = {
        "screening": screening,
        "booking_details": booking_details,
        "total_price_paid": total_price_paid,
        "booking_id": pk,
    }
    
    return render(request, "booking/purchase_seats.html", context)


def reserve_seats(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    screening = get_object_or_404(Screening, pk=pk)
    selected_seats_raw = request.POST.get("selected_seats", "")

    selected_seats =[
        id.strip()
        for id in selected_seats_raw.split(",")
        if id.strip()
    ]

    with transaction.atomic():
        seats = ScreeningSeat.objects.select_for_update().filter(
            screening=screening,
            seat__id__in=selected_seats,
            seat_status=ScreeningSeat.Status.AVAILABLE,
        )

        if seats.count() != len(selected_seats):
            return redirect("booking:seat-selector", pk=pk)
        
        booking = Booking.objects.create()

        for seat in seats:
            seat.seat_status = ScreeningSeat.Status.HELD
            seat.held_until = timezone.now() + timedelta(minutes=5)
            seat.save()

            BookingDetail.objects.create(
                booking=booking,
                screening_seat=seat,
                price_paid_cents=seat.screening.base_price_cents + seat.seat.type_seat.price_modifier_cents
            )

    return redirect("booking:purchase-seats", pk=booking.id)

def payment(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    booking = get_object_or_404(Booking, pk=pk)
    booking_details = BookingDetail.objects.select_related("screening_seat").select_for_update().filter(booking=pk)

    with transaction.atomic():
        for detail in booking_details:
            ss = detail.screening_seat
            ss.seat_status = ScreeningSeat.Status.SOLD
            ss.held_until = None
            ss.save()
        
        booking.status = Booking.Status.FINISHED
        booking.save()

    return redirect("booking:booking-sumary", pk=booking.id)


def booking_sumary(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    seats = get_list_or_404(BookingDetail, booking=booking)
    data = seats[0]
    screening = data.screening_seat.screening
    context = {
        "booking": booking,
        "seats": seats,
        "screening": screening,
    }

    return render(request, "booking/booking_sumary.html", context)