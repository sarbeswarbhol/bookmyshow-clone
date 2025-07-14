from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

# 🔹 Mixin to reuse authentication check
class RequireAuthenticated:
    def check_auth(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")


# 🔹 Only movie_owner role
class IsMovieOwner(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'movie_owner':
            raise PermissionDenied("Only movie owners are allowed.")
        return True


# 🔹 Movie Owner + Creator of the movie
class IsMovieOwnerAndCreator(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        return True

    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.user.role != 'movie_owner' or request.user != obj.created_by:
            raise PermissionDenied("Only the movie creator (movie owner) can perform this action.")
        return True


# 🔹 Admin, Superuser, or Staff
class IsAdminOrStaff(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if not (request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'):
            raise PermissionDenied("Only admin, superuser, or staff can access this.")
        return True


# 🔹 Only theater_owner role
class IsTheaterOwner(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'theater_owner':
            raise PermissionDenied("Only theater owners are allowed.")
        return True


# 🔹 Regular user only
class IsRegularUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'user':
            raise PermissionDenied("Only regular users are allowed.")
        return True


# 🔹 Creator of the object or read-only access
class IsOwnerOrReadOnly(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        self.check_auth(request)
        if request.user != obj.created_by:
            raise PermissionDenied("Only the owner can modify this resource.")
        return True


# 🔹 Object owner only (full access)
class IsOwner(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if request.user != obj.created_by:
            raise PermissionDenied("Only the owner can access this resource.")
        return True


# 🔹 Movie creator or admin/superuser/staff
class IsMovieOwnerOrAdmin(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if not (
            request.user == obj.created_by or
            request.user.is_superuser or
            request.user.is_staff or
            request.user.role == 'admin'
        ):
            raise PermissionDenied("Only the movie creator or admin/superuser/staff can perform this action.")
        return True


# 🔹 Only the user themselves or admin
class IsSelfOrAdmin(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if not (
            request.user == obj or
            request.user.is_superuser or
            request.user.is_staff or
            request.user.role == 'admin'
        ):
            raise PermissionDenied("Only the user or admin can perform this action.")
        return True


# 🔹 Authenticated and active user
class IsAuthenticatedAndActive(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if not request.user.is_active:
            raise PermissionDenied("Inactive users cannot access this.")
        return True


# 🔹 Only review creator can modify/delete
class IsReviewAuthor(BasePermission, RequireAuthenticated):
    def has_object_permission(self, request, view, obj):
        self.check_auth(request)
        if obj.user != request.user:
            raise PermissionDenied("Only the review author can modify or delete this review.")
        return True


# 🔹 Admin role only
class IsAdminUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users are allowed.")
        return True


# 🔹 Only superuser
class IsSuperUser(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers are allowed.")
        return True


# 🔹 Superuser or admin
class IsSuperUserOrAdmin(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if not (request.user.is_superuser or request.user.role == 'admin'):
            raise PermissionDenied("Only superuser or admin users are allowed.")
        return True


# 🔹 Staff or admin
class IsStaffOrAdmin(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if not (request.user.is_staff or request.user.role == 'admin'):
            raise PermissionDenied("Only staff or admin users are allowed.")
        return True


# 🔹 Admin can write, others read-only
class IsAdminOrReadOnly(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        self.check_auth(request)
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can perform write actions.")
        return True


# 🔹 Authenticated users can read-only
class IsAuthenticatedReadOnly(BasePermission, RequireAuthenticated):
    def has_permission(self, request, view):
        self.check_auth(request)
        if request.method not in SAFE_METHODS:
            raise PermissionDenied("Read-only access is allowed.")
        return True
