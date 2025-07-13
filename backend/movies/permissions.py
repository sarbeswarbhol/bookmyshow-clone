from rest_framework.permissions import BasePermission, SAFE_METHODS

# 🔹 Only movie_owner role
class IsMovieOwner(BasePermission):
    """
    Allows access only to users with role 'movie_owner'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'movie_owner'


# 🔹 Movie Owner + Creator of the movie
class IsMovieOwnerAndCreator(BasePermission):
    """
    Only the creator who is a movie_owner can access
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by and request.user.role == 'movie_owner'


# 🔹 Admin, Superuser, or Staff
class IsAdminOrStaff(BasePermission):
    """
    Only for admin, superuser, or staff members
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'
        )


# 🔹 Theater Owner only
class IsTheaterOwner(BasePermission):
    """
    Only theater_owner role allowed
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'theater_owner'


# 🔹 Creator of the object or read-only access
class IsOwnerOrReadOnly(BasePermission):
    """
    Full access to owner, read-only for others
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user


# 🔹 Either movie owner (creator) or admin/superuser/staff
class IsMovieOwnerOrAdmin(BasePermission):
    """
    Movie creator OR superuser/staff/admin
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user == obj.created_by or 
                request.user.is_superuser or 
                request.user.is_staff or 
                request.user.role == 'admin'
            )
        )


# 🔹 Only the user themselves or admin
class IsSelfOrAdmin(BasePermission):
    """
    User can modify their own profile or admin can
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj or
            request.user.is_superuser or
            request.user.is_staff or
            request.user.role == 'admin'
        )


# 🔹 Authenticated and active user
class IsAuthenticatedAndActive(BasePermission):
    """
    Requires the user to be authenticated and not disabled
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active


# 🔹 Only review creator can modify/delete
class IsReviewAuthor(BasePermission):
    """
    Only the review author can update/delete the review
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user




class IsAdminUser(BasePermission):
    """Allow only admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTheaterOwner(BasePermission):
    """Allow only theater owners."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'theater_owner'


class IsMovieOwner(BasePermission):
    """Allow only movie owners."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'movie_owner'


class IsRegularUser(BasePermission):
    """Allow only regular users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'


class IsAdminOrReadOnly(BasePermission):
    """Allow only admin to write, others can read-only."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrReadOnly(BasePermission):
    """Allow object creator to write; others read-only."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.created_by


class IsOwner(BasePermission):
    """Only allow object creator to access/modify."""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by


class IsSuperUserOrAdmin(BasePermission):
    """Allow only superuser or admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin')


class IsSuperUser(BasePermission):
    """Allow only Django superuser."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsStaffOrAdmin(BasePermission):
    """Allow Django staff or admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')


class IsAuthenticatedReadOnly(BasePermission):
    """Authenticated users can read-only access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS
