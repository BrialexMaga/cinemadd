from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie


def index(request):
    pass

def movie_list(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, "booking/movies.html", context)