# Movie Ticket Booking System — Django + DRF

A complete backend for movie ticket booking with JWT authentication, concurrency-safe seat booking, cancellation, and Swagger API docs at `/swagger/`.

## Features
- **Auth:** Signup, Login via JWT (access/refresh)
- **Models:** Movie, Show, Booking (booked/cancelled)
- **APIs:** Movies, shows, book seat, cancel, my bookings
- **Business rules:** Prevent double booking and overbooking; cancelling frees the seat
- **Docs:** Swagger UI via drf-spectacular with BearerAuth

## Tech
- Django, Django REST Framework
- djangorestframework-simplejwt
- drf-spectacular

## Setup

1. **Clone & install**
   ```bash
   git clone <your-repo-url>
   cd movie_booking
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
