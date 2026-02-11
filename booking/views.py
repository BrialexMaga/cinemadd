from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Screening, ScreeningSeat
from collections import defaultdict


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