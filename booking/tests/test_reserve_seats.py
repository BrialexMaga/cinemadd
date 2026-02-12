from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from booking.models import Movie, Room, Screening, Seat, ScreeningSeat, TypeSeat


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

        self.url = reverse("reserve-seats", args=[self.screening.id])