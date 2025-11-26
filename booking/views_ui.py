from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Show, Booking

def movies_page(request):
    movies = Movie.objects.all()
    return render(request, "booking/movies.html", {"movies": movies})

def shows_page(request, movie_id):
    shows = Show.objects.filter(movie_id=movie_id)
    return render(request, "booking/shows.html", {"shows": shows})

@login_required
def my_bookings_page(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking/my_bookings.html", {"bookings": bookings})
