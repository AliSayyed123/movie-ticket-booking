from rest_framework.permissions import BasePermission

class IsAuthenticatedForBookings(BasePermission):
    """
    Require auth for booking-related endpoints.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
