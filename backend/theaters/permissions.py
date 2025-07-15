from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


# 🔹 Reusable Mixin: Enforces authentication
class RequireAuthenticated:
    def check_auth(self, request):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")
            

# ✅ Only users with the 'theater_owner' role
class IsTheaterOwner(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'theater_owner':
            raise PermissionDenied("Only users with the 'theater_owner' role are allowed.")
        return True


# ✅ Only theater_owner AND creator of the object
class IsTheaterOwnerAndCreator(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.user.role != 'theater_owner':
            raise PermissionDenied("Only theater owners can access this resource.")
        if request.user != obj.created_by:
            raise PermissionDenied("You can only manage resources you created.")
        return True


# ✅ Public can read, only theater_owner+creator can write
class IsTheaterOwnerOrReadOnly(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        self.check_auth(request)
        return request.user.role == 'theater_owner'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.created_by and request.user.role == 'theater_owner'


# ✅ Public can read, only admin/superuser can write
class IsAdminOrReadOnly(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        self.check_auth(request)
        return request.user.is_superuser or request.user.role == 'admin'
