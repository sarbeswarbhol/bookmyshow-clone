from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


# 🔹 Reusable authentication check mixin
class RequireAuthenticated:
    """
    Mixin for enforcing authentication manually in permission classes.
    """
    def check_auth(self, request):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")


# 🔹 Regular authenticated user (role: user)
class IsRegularUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if getattr(request.user, 'role', None) != 'user':
            raise PermissionDenied("Only regular users can perform this action.")
        return True


# 🔹 Booking Owner or Read-Only
class IsBookingOwnerOrReadOnly(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.method in SAFE_METHODS:
            return True
        if obj.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to modify this booking.")


# 🔹 Payment Owner Only (user who made the booking)
class IsPaymentOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to access this payment.")


# 🔹 Ticket Owner or Admin
class IsTicketOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to access this ticket.")

class IsTheaterOwnerOfShowSeatPricing(BasePermission, RequireAuthenticated):
    """
    Allows only the owner of the theater (via show) or staff/superuser.
    """
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)

        if obj.show.theater.created_by == request.user or request.user.is_staff or request.user.is_superuser:
            return True

        raise PermissionDenied("You do not have permission to access or modify this seat pricing.")