from django.urls import path
from .views import (
    CastMemberRestoreView,
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    MovieRestoreView,
    CastMemberListView,
    CastMemberCreateView,
    CastMemberDetailView,
    CastMemberDeleteView,
    CastMemberUpdateView,
    ReviewDeleteView,
    ReviewListCreateView,
    ReviewRestoreView,
    ReviewUpdateView
)

urlpatterns = [
    # Cast Members — put these FIRST
    path('cast/', CastMemberListView.as_view(), name='cast-list'),
    path('cast/create/', CastMemberCreateView.as_view(), name='cast-create'),
    path('cast/<int:id>/', CastMemberDetailView.as_view(), name='cast-detail'),
    path('cast/<int:id>/delete/', CastMemberDeleteView.as_view(), name='cast-delete'),
    path('cast/<int:id>/update/', CastMemberUpdateView.as_view(), name='cast-update'),
    path('cast/<int:id>/restore/', CastMemberRestoreView.as_view(), name='cast-restore'),

    # Movie routes — put these AFTER cast
    path('', MovieListView.as_view(), name='movie-list'),
    path('create/', MovieCreateView.as_view(), name='movie-create'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('<slug:slug>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('<slug:slug>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path('<slug:slug>/restore/', MovieRestoreView.as_view(), name='movie-restore'),

    # Reviews (nested under movies)
    path('<slug:slug>/reviews/', ReviewListCreateView.as_view(), name='movie-reviews'),
    path('<slug:slug>/reviews/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
    path('<slug:slug>/reviews/update/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
    path('<slug:slug>/reviews/restore/<int:pk>/', ReviewRestoreView.as_view(), name='review-restore'),
]
