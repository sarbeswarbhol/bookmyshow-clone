from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# 🔹 Mixin for reusability
class RequireAuthenticated:
    def check_auth(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")


# 🔹 Only theater owners
class IsTheaterOwner(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'theater_owner':
            raise PermissionDenied("Only theater owners are allowed.")
        return True


# 🔹 Theater owner AND creator of the object
class IsTheaterOwnerAndCreator(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.user.role != 'theater_owner' or request.user != obj.created_by:
            raise PermissionDenied("Only the theater owner who created this resource can access it.")
        return True
