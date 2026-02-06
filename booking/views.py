from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie


def start(request):
    return render(request, "booking/start_project.html")

def movie_list(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, "booking/movies.html", context)