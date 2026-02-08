from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Screening


def start(request):
    return render(request, "booking/start_project.html")

def movie_list(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, "booking/movies.html", context)

def seat_selector(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    context = {"screening": screening}
    return render(request, "booking/seat_selector.html", context)