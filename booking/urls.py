from django.urls import path

from . import views

app_name = "booking"
urlpatterns = [
    path("", views.movie_list, name="movie-list"),
]