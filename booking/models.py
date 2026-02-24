from django.db import models
from django.utils import timezone

class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveSmallIntegerField()
    poster_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Room {self.number}"

class TypeSeat(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    price_modifier_cents = models.IntegerField()

    def __str__(self):
        return self.name

class Screening(models.Model):
    id = models.BigAutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    base_price_cents = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie} @ {self.start_time:%Y-%m-%d %H:%M}"

class Seat(models.Model):
    id = models.BigAutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seats")
    type_seat = models.ForeignKey(TypeSeat, on_delete=models.PROTECT)
    row_letter = models.CharField(max_length=2)
    column_number = models.PositiveSmallIntegerField()

    @property
    def code_only(self):
        return f"{self.row_letter}{self.column_number}"

    def __str__(self):
        return f"Seat {self.row_letter}{self.column_number}"

class ScreeningSeat(models.Model):
    class Status(models.IntegerChoices):
        AVAILABLE = 1, "Available"
        HELD = 2, "Held"
        SOLD = 3, "Sold"

    id = models.BigAutoField(primary_key=True)
    screening = models.ForeignKey(Screening, on_delete=models.PROTECT, related_name="screening_seats")
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    seat_status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.AVAILABLE)
    held_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.seat} - {self.screening}"

    class Meta:
        unique_together = ("screening", "seat")

class Booking(models.Model):
    class Status(models.IntegerChoices):
        ONGOING = 1, "Ongoing"
        FINISHED = 2, "Finished"
        CANCELED = 3, "Canceled"

    id = models.BigAutoField(primary_key=True)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.ONGOING)

    def __str__(self):
        return f"Booking #{self.id} ({self.get_status_display()})"

class BookingDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_details")
    screening_seat = models.ForeignKey(ScreeningSeat, on_delete=models.PROTECT)
    price_paid_cents = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.screening_seat} in {self.booking}"

    class Meta:
        unique_together = ("booking", "screening_seat")