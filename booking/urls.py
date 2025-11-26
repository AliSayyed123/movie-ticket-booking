from django.urls import path
from .views import (
    SignupView, LoginView, MovieListView, MovieShowsListView,
    BookSeatView, CancelBookingView, MyBookingsListView
)
from .views_ui import movies_page, shows_page, my_bookings_page

urlpatterns = [
    # Auth
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    # Movies and shows (API)
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:id>/shows/', MovieShowsListView.as_view(), name='movie-shows'),

    # Bookings (JWT required)
    path('shows/<int:id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', MyBookingsListView.as_view(), name='my-bookings'),

    # UI routes
    path('ui/movies/', movies_page, name='movies-page'),
    path('ui/movies/<int:movie_id>/shows/', shows_page, name='shows-page'),
    path('ui/my-bookings/', my_bookings_page, name='my-bookings-page'),
]
