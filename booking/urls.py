from django.urls import path

from . import views

app_name = "booking"
urlpatterns = [
    path("", views.start, name="start"),
    path("movies/", views.movie_list, name="movie-list"),
    path("<int:pk>/seats/", views.seat_selector, name="seat-selector"),
]