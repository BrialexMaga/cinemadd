# 🎬 Cinemadd – Cinema Booking Simulator

Cinemadd is a small web app that simulates how a cinema booking system works. Users can browse screenings, select seats, place temporary holds, and finalize a booking. The project focuses on realistic backend behavior like seat availability, concurrency safety, and state transitions.

## ✨ Features

- Browse movies and screenings
- Seat selection per screening
- Concurrency-safe reservations (no double-booking)
- Seat states: Available → Held → Sold
- Temporary seat holds with expiration
- Booking flow with confirmation step
- Admin-friendly data models for screenings, rooms, and seats
- Automated tests for core booking logic

## 🚀 Getting Started (Local)

1. Clone & set up environment

    ```bash
    git clone https://github.com/BrialexMaga/cinemadd.git
    cd cinemadd
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2. Configure environment variables

    Copy the example file and fill your own values:

    ```bash
    cp env.example .env
    ```

    Edit .env with your local PostgreSQL credentials.


3. Run migrations & seed data

    ```
    python manage.py migrate
    python manage.py createsuperuser
    ```
4. Start the server

    ```
    python manage.py runserver
    ```

    Open: localhost:8000

## Running Tests

    python manage.py test


## 🔁 Booking Flow (MVP)

1. User selects seats for a screening
2. Seats are HELD with a 5-minute expiration
3. User confirms the booking
4. Seats become SOLD and booking is FINISHED
5. If confirmation fails or expires, seats are released

## 📌 Notes

This is an educational/demo project designed to model real-world booking behavior (transactions, locking, and state transitions). It’s not production-hardened but aims to reflect how a cinema booking flow should work under concurrent usage.