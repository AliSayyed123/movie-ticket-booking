from django.conf import settings
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f'{self.movie.title} @ {self.screen_name} on {self.date_time}'

class Booking(models.Model):
    STATUS_BOOKED = 'booked'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_BOOKED, 'Booked'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('show', 'seat_number', 'status')  # helps prevent duplicate active bookings
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking {self.id} - seat {self.seat_number} ({self.status})'
