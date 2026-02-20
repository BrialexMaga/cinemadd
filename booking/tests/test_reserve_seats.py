from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from booking.models import Movie, Room, Screening, Seat, ScreeningSeat, TypeSeat, Booking, BookingDetail


class ReserveSeatsTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(name="Inception", duration_minutes=60)
        self.room = Room.objects.create(number=1)
        self.type_seat = TypeSeat.objects.create(name="Standard", price_modifier_cents=0)

        self.screening = Screening.objects.create(
            movie=self.movie,
            room=self.room,
            start_time=timezone.now(),
            base_price_cents=1200,
        )

        self.seat1 = Seat.objects.create(
            row_letter="A", 
            column_number=1, 
            room=self.room, 
            type_seat=self.type_seat,
        )
        
        self.seat2 = Seat.objects.create(
            row_letter="A", 
            column_number=2, 
            room=self.room, 
            type_seat=self.type_seat,
        )

        self.ss_a1 = ScreeningSeat.objects.create(
            screening=self.screening,
            seat=self.seat1,
        )

        self.ss_a2 = ScreeningSeat.objects.create(
            screening=self.screening,
            seat=self.seat2,
        )

        self.url = reverse("booking:reserve-seats", args=[self.screening.id])
    
    def test_successful_reservation_holds_seats_and_creates_booking(self):
        response = self.client.post(self.url, {
            "selected_seats": f"{self.seat1.id},{self.seat2.id}"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(BookingDetail.objects.count(), 2)

        self.ss_a1.refresh_from_db()
        self.ss_a2.refresh_from_db()

        self.assertEqual(self.ss_a1.seat_status, ScreeningSeat.Status.HELD)
        self.assertEqual(self.ss_a2.seat_status, ScreeningSeat.Status.HELD)

        self.assertIsNotNone(self.ss_a1.held_until)
    

    def test_reservation_fails_if_seat_not_available(self):
        self.ss_a1.seat_status = ScreeningSeat.Status.HELD
        self.ss_a1.save()

        response = self.client.post(self.url, {
            "selected_seats": f"{self.seat1.id}"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertEqual(BookingDetail.objects.count(), 0)

    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
