from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


# 🔹 Mixin for authentication enforcement
class RequireAuthenticated:
    """
    Mixin for enforcing authentication in permission classes.
    """
    def check_auth(self, request):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")


# 🔹 Regular user with role 'user' only
class IsRegularUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if getattr(request.user, 'role', None) != 'user':
            raise PermissionDenied("Only regular users can perform this action.")
        return True


# 🔹 Booking owner or read-only
class IsBookingOwnerOrReadOnly(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.method in SAFE_METHODS:
            return True
        if obj.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to modify this booking.")


# 🔹 Only booking owner can access the payment
class IsPaymentOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to access this payment.")


# 🔹 Only ticket owner or admin
class IsTicketOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to access this ticket.")


# 🔹 Only theater owner (via show) can set/update pricing
class IsTheaterOwnerOfShowSeatPricing(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.show.theater.created_by == request.user or request.user.is_staff or request.user.is_superuser:
            return True
        raise PermissionDenied("You do not have permission to modify this seat pricing.")
