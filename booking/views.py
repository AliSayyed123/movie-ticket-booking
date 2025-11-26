from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiExample

from .models import Movie, Show, Booking
from .serializers import (
    SignupSerializer, MovieSerializer, ShowSerializer,
    BookingSerializer, BookSeatSerializer
)
from .permissions import IsAuthenticatedForBookings
from .services import book_seat, cancel_booking, BookingError

# Authentication

class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    @extend_schema(
        tags=['Auth'],
        request=SignupSerializer,
        responses={201: SignupSerializer},
        examples=[
            OpenApiExample(
                'Signup example',
                value={"username": "alice", "email": "alice@example.com", "password": "secret123"},
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Auth'],
        responses={
            200: OpenApiResponse(description='Returns access and refresh JWT tokens')
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Public data

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=['Movies'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MovieShowsListView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Shows'],
        parameters=[OpenApiParameter(name='id', location=OpenApiParameter.PATH, description='Movie ID')]
    )
    def get_queryset(self):
        movie_id = self.kwargs['id']
        return Show.objects.filter(movie_id=movie_id).order_by('date_time')

# Booking actions (JWT required)

class BookSeatView(APIView):
    permission_classes = [IsAuthenticatedForBookings]

    @extend_schema(
        tags=['Bookings'],
        request=BookSeatSerializer,
        responses={201: BookingSerializer, 400: OpenApiResponse(description='Booking error')},
        parameters=[OpenApiParameter(name='id', location=OpenApiParameter.PATH, description='Show ID')]
    )
    def post(self, request, id):
        serializer = BookSeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seat_number = serializer.validated_data['seat_number']
        try:
            booking = book_seat(request.user, id, seat_number)
        except BookingError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticatedForBookings]

    @extend_schema(
        tags=['Bookings'],
        responses={200: BookingSerializer, 400: OpenApiResponse(description='Cancellation error')},
        parameters=[OpenApiParameter(name='id', location=OpenApiParameter.PATH, description='Booking ID')]
    )
    def post(self, request, id):
        try:
            booking = cancel_booking(request.user, id)
        except BookingError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)

class MyBookingsListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedForBookings]

    @extend_schema(tags=['Bookings'])
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')
