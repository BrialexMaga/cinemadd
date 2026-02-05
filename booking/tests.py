from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Movie, Room, Screening


class MovieListViewTests(TestCase):
    def test_movie_list_page_exists(self):
        response = self.client.get(reverse("booking:movie-list"))
        self.assertEqual(response.status_code, 200)
    
    def test_movies_are_listed(self):
        Movie.objects.create(name="Interstellar", duration_seconds=11)
        Movie.objects.create(name="Inception", duration_seconds=12)

        response = self.client.get(reverse("booking:movie-list"))

        self.assertContains(response, "Interstellar")
        self.assertContains(response, "Inception")
    
    def test_screenings_are_shown_under_movies(self):
        movie = Movie.objects.create(name="Interstellar", duration_seconds=11)
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