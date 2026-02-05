from django.contrib import admin
from .models import Booking, BookingDetail, ScreeningSeat, Movie, Room, Seat, TypeSeat, Screening

# Register your models here.
admin.site.register(Booking)
admin.site.register(BookingDetail)
admin.site.register(ScreeningSeat)
admin.site.register(Movie)
admin.site.register(Room)
admin.site.register(Seat)
admin.site.register(TypeSeat)
admin.site.register(Screening)