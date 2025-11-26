
### Movie Ticket Booking System (Django + DRF)

A backend system for booking movie tickets, built with **Django** and **Django REST Framework**.  
Includes **JWT authentication**, **seat booking logic**, and **Swagger API documentation**.

---

##  Where this runs
- Runs locally on your machine using **Python** and **Django’s development server**.
- Default server address:  
   `http://127.0.0.1:8000/`
- API documentation (Swagger UI):  
   `http://127.0.0.1:8000/swagger/`
- Admin panel:  
   `http://127.0.0.1:8000/admin/`
- Optional HTML UI pages:  
   `http://127.0.0.1:8000/ui/movies/`

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
   git clone https://github.com/AliSayyed123/movie-ticket-booking
   cd movie_booking
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
