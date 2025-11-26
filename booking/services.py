from django.db import transaction
from django.db.models import Q, Count
from .models import Show, Booking

class BookingError(Exception):
    pass

@transaction.atomic
def book_seat(user, show_id, seat_number):
    """
    Concurrency-safe booking:
    - prevent double booking of a seat for a show
    - prevent overbooking beyond total_seats
    """
    show = Show.objects.select_for_update().get(id=show_id)

    if seat_number < 1 or seat_number > show.total_seats:
        raise BookingError(f'Seat number must be between 1 and {show.total_seats}.')

    # Check if seat already booked and not cancelled
    exists = Booking.objects.select_for_update().filter(
        show=show,
        seat_number=seat_number,
        status=Booking.STATUS_BOOKED
    ).exists()
    if exists:
        raise BookingError('Seat already booked.')

    # Capacity check: count active bookings
    active_count = Booking.objects.filter(show=show, status=Booking.STATUS_BOOKED).count()
    if active_count >= show.total_seats:
        raise BookingError('Show is fully booked.')

    booking = Booking.objects.create(
        user=user,
        show=show,
        seat_number=seat_number,
        status=Booking.STATUS_BOOKED
    )
    return booking

@transaction.atomic
def cancel_booking(user, booking_id):
    """
    Cancelling frees the seat (status -> cancelled).
    Only owner can cancel.
    """
    booking = Booking.objects.select_for_update().get(id=booking_id)
    if booking.user_id != user.id:
        raise BookingError('You can only cancel your own bookings.')
    if booking.status == Booking.STATUS_CANCELLED:
        return booking
    booking.status = Booking.STATUS_CANCELLED
    booking.save(update_fields=['status'])
    return booking
