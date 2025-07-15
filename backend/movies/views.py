from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Movie, CastMember, Review
from .serializers import (
    MovieSerializer,
    MovieCreateUpdateSerializer,
    CastMemberSerializer,
    CastMemberDetailSerializer,
    ReviewSerializer
)
from .permissions import (
    IsAdminOrStaff,
    IsMovieOwner,
    IsMovieOwnerAndCreator,
    IsMovieOwnerOrAdmin,
    IsAdminOrStaff,
    IsReviewAuthor
)

# 🔹 Movies
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.filter(is_deleted=False)
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(is_deleted=False)
    serializer_class = MovieSerializer
    lookup_field = 'slug'

class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = [IsMovieOwner]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MovieUpdateView(generics.UpdateAPIView):
    queryset = Movie.objects.filter(is_deleted=False)
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = [IsMovieOwnerAndCreator]
    lookup_field = 'slug'

class MovieDeleteView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsMovieOwnerAndCreator]
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Movie deleted successfully."}, status=status.HTTP_200_OK)

class MovieRestoreView(generics.UpdateAPIView):
    queryset = Movie.all_objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsMovieOwnerOrAdmin]
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.is_deleted = False
        movie.save()
        return Response({"message": "Movie restored successfully."}, status=status.HTTP_200_OK)

# 🔹 Cast
class CastMemberListView(generics.ListAPIView):
    queryset = CastMember.objects.filter(is_deleted=False)
    serializer_class = CastMemberSerializer

class CastMemberCreateView(generics.CreateAPIView):
    queryset = CastMember.objects.all()
    serializer_class = CastMemberSerializer
    permission_classes = [IsAdminOrStaff]

class CastMemberDetailView(generics.RetrieveAPIView):
    queryset = CastMember.objects.filter(is_deleted=False)
    serializer_class = CastMemberDetailSerializer
    lookup_field = 'id'

class CastMemberUpdateView(generics.UpdateAPIView):
    queryset = CastMember.objects.filter(is_deleted=False)
    serializer_class = CastMemberSerializer
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'

class CastMemberDeleteView(generics.DestroyAPIView):
    queryset = CastMember.objects.all()
    serializer_class = CastMemberSerializer
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Cast member soft-deleted successfully."}, status=status.HTTP_200_OK)

class CastMemberRestoreView(generics.UpdateAPIView):
    queryset = CastMember.all_objects.all()
    serializer_class = CastMemberSerializer
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = False
        instance.save()
        return Response({"message": "Cast member restored successfully."}, status=status.HTTP_200_OK)

# 🔹 Reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = []  # Auth check is handled in perform_create

    def get_queryset(self):
        return Review.objects.filter(movie__slug=self.kwargs['slug'], is_deleted=False)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        movie = Movie.objects.get(slug=self.kwargs['slug'])
        user = self.request.user

    # Check if user already reviewed this movie
        if Review.objects.filter(user=user, movie=movie, is_deleted=False).exists():
            raise ValidationError("You have already submitted a review for this movie.")
        serializer.save(user=self.request.user, movie=movie)

class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.filter(is_deleted=False)
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthor]
    lookup_field = 'pk'

    def get_queryset(self):
         return self.queryset.filter(movie__slug=self.kwargs['slug'])
     
class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.all_objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthor]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(movie__slug=self.kwargs['slug'])

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Review.DoesNotExist:
            return Response({"detail": "Review not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return Response({"message": "Review deleted successfully."}, status=status.HTTP_200_OK)
    
class ReviewRestoreView(generics.UpdateAPIView):
    queryset = Review.all_objects.all()  # ✅ allows soft-deleted reviews
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthor]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_deleted:
            return Response(
                {"detail": "Review is already active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.is_deleted = False
        instance.save()
        return Response(
            {"message": "Review restored successfully."},
            status=status.HTTP_200_OK
        )
