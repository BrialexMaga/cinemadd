from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Movie, Room, Screening, Seat, ScreeningSeat, TypeSeat


class MovieListViewTests(TestCase):
    def test_movie_list_page_exists(self):
        response = self.client.get(reverse("booking:movie-list"))
        self.assertEqual(response.status_code, 200)
    
    def test_movies_are_listed(self):
        Movie.objects.create(name="Interstellar", duration_minutes=11)
        Movie.objects.create(name="Inception", duration_minutes=12)

        response = self.client.get(reverse("booking:movie-list"))

        self.assertContains(response, "Interstellar")
        self.assertContains(response, "Inception")
    
    def test_screenings_are_shown_under_movies(self):
        movie = Movie.objects.create(name="Interstellar", duration_minutes=11)
        room = Room.objects.create(number=2)

        Screening.objects.create(
            movie=movie,
            room=room,
            start_time=timezone.now(),
            base_price_cents = 1200
        )

        response = self.client.get(reverse("booking:movie-list"))

        self.assertContains(response, "Interstellar")
        self.assertContains(response, 2)
    

class SeatSelectorViewTest(TestCase):
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

        self.seat_a1 = Seat.objects.create(
            row_letter="A", 
            column_number=1, 
            room=self.room, 
            type_seat=self.type_seat,
        )
        
        self.seat_a2 = Seat.objects.create(
            row_letter="A", 
            column_number=2, 
            room=self.room, 
            type_seat=self.type_seat,
        )

        self.ss_a1 = ScreeningSeat.objects.create(
            screening=self.screening,
            seat=self.seat_a1,
        )

        self.ss_a2 = ScreeningSeat.objects.create(
            screening=self.screening,
            seat=self.seat_a2,
        )
        

    def test_seat_selector_page_exist(self):
        url = reverse("booking:seat-selector", args=[self.screening.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
    
    def test_seats_are_in_context(self):
        url = reverse("booking:seat-selector", args=[self.screening.id])
        response = self.client.get(url)

        self.assertIn("seats_by_row", response.context)