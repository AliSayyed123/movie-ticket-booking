from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Movie, Show, Booking
from datetime import datetime, timezone

class BookingLogicTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bob', password='secret123')
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(
            movie=self.movie, screen_name='Screen 1',
            date_time=datetime(2030, 1, 1, 18, 0, tzinfo=timezone.utc),
            total_seats=2
        )
        # Login
        resp = self.client.post('/login', {'username':'bob','password':'secret123'}, format='json')
        self.access = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_prevent_double_booking(self):
        r1 = self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(r1.status_code, 201)
        r2 = self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(r2.status_code, 400)

    def test_prevent_overbooking(self):
        self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 2}, format='json')
        r3 = self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 2}, format='json')
        self.assertEqual(r3.status_code, 400)

    def test_cancel_frees_seat(self):
        r1 = self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 2}, format='json')
        booking_id = r1.data['id']
        r2 = self.client.post(f'/bookings/{booking_id}/cancel/', {}, format='json')
        self.assertEqual(r2.status_code, 200)
        r3 = self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 2}, format='json')
        self.assertEqual(r3.status_code, 201)
