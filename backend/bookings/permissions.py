from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


# 🔹 Reusable authentication check mixin
class RequireAuthenticated:
    def check_auth(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")


# 🔹 Regular authenticated user (role: user)
class IsRegularUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'user':
            raise PermissionDenied("Only regular users can perform this action.")
        return True


# 🔹 Booking Owner or Read-Only
class IsBookingOwnerOrReadOnly(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.method in SAFE_METHODS:
            return True
        if obj.user != request.user and not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to modify this booking.")
        return True


# 🔹 Payment Owner Only (user who made the booking)
class IsPaymentOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user != request.user and not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to access this payment.")
        return True


# 🔹 Ticket Owner or Admin
class IsTicketOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.booking.user != request.user and not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to access this ticket.")
        return True
