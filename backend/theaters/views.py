# theaters/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Theater, Show
from .serializers import TheaterSerializer, ShowSerializer
from .permissions import IsTheaterOwner, IsTheaterOwnerAndCreator

# 🎭 Theater Views
class TheaterListView(generics.ListAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

class TheaterDetailView(generics.RetrieveAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    lookup_field = 'slug'

class TheaterCreateView(generics.CreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsTheaterOwner]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TheaterUpdateView(generics.UpdateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsTheaterOwnerAndCreator]
    lookup_field = 'slug'

class TheaterDeleteView(generics.DestroyAPIView):
    queryset = Theater.all_objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsTheaterOwnerAndCreator]
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Theater deleted successfully."}, status=status.HTTP_200_OK)

class TheaterRestoreView(generics.UpdateAPIView):
    queryset = Theater.all_objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsTheaterOwnerAndCreator]
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        theater = self.get_object()
        if not theater.is_deleted:
            return Response({"message": "Theater is already active."}, status=status.HTTP_400_BAD_REQUEST)
        theater.is_deleted = False
        theater.save()
        return Response({"message": "Theater restored successfully."}, status=status.HTTP_200_OK)


# 🎬 Show Views (Nested)
class ShowListByTheaterView(generics.ListAPIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(theater__slug=self.kwargs['slug'], is_deleted=False)

class ShowCreateUnderTheaterView(generics.CreateAPIView):
    serializer_class = ShowSerializer
    permission_classes = [IsTheaterOwner]

    def perform_create(self, serializer):
        theater = Theater.objects.get(slug=self.kwargs['slug'])
        if theater.created_by != self.request.user:
            raise PermissionDenied("You can only create shows for your own theater.")
        serializer.save(theater=theater, created_by=self.request.user)

# Flat Show Views for details/edit/delete/restore
class ShowDetailView(generics.RetrieveAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

class ShowUpdateView(generics.UpdateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsTheaterOwnerAndCreator]

class ShowDeleteView(generics.DestroyAPIView):
    queryset = Show.all_objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsTheaterOwnerAndCreator]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Show deleted successfully."}, status=status.HTTP_200_OK)

class ShowRestoreView(generics.UpdateAPIView):
    queryset = Show.all_objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsTheaterOwnerAndCreator]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        show = self.get_object()
        if not show.is_deleted:
            return Response({"message": "Show is already active."}, status=status.HTTP_400_BAD_REQUEST)
        show.is_deleted = False
        show.save()
        return Response({"message": "Show restored successfully."}, status=status.HTTP_200_OK)
