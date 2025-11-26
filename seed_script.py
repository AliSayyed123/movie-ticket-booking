import os
import django
from datetime import datetime, timedelta, timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

from django.contrib.auth.models import User
from booking.models import Movie, Show

def run():
    if not User.objects.filter(username='demo').exists():
        User.objects.create_user(username='demo', password='demo123', email='demo@example.com')
        print('Created demo user: demo / demo123')

    movie, _ = Movie.objects.get_or_create(title='Interstellar', duration_minutes=169)
    now = datetime.now(timezone.utc)
    Show.objects.get_or_create(movie=movie, screen_name='PVR A', date_time=now + timedelta(days=1, hours=18), total_seats=5)
    Show.objects.get_or_create(movie=movie, screen_name='PVR B', date_time=now + timedelta(days=2, hours=20), total_seats=3)
    print('Seeded movies and shows.')

if __name__ == '__main__':
    run()
