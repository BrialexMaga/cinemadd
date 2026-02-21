from django.urls import path

from . import views

app_name = "booking"
urlpatterns = [
    path("", views.start, name="start"),
    path("movies/", views.movie_list, name="movie-list"),
    path("<int:pk>/seats/", views.seat_selector, name="seat-selector"),
    path("<int:pk>/reservation/", views.reserve_seats, name="reserve-seats"),
    path("<int:pk>/purchase/", views.purchase_seats, name="purchase-seats"),
    path("<int:pk>/payment/", views.payment, name="payment-finished"),
    path("<int:pk>/sumary", views.booking_sumary, name="booking-sumary"),
]