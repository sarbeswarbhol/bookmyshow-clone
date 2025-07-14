# theaters/urls.py
from django.urls import path
from .views import (
    TheaterListView, TheaterCreateView, TheaterDetailView, TheaterRestoreView, TheaterUpdateView, TheaterDeleteView,
    ShowListByTheaterView, ShowCreateUnderTheaterView, ShowDetailView,
    ShowUpdateView, ShowDeleteView, ShowRestoreView
)

urlpatterns = [
    # Theaters
    path('', TheaterListView.as_view(), name='theater-list'),
    path('create/', TheaterCreateView.as_view(), name='theater-create'),
    path('<slug:slug>/', TheaterDetailView.as_view(), name='theater-detail'),
    path('<slug:slug>/update/', TheaterUpdateView.as_view(), name='theater-update'),
    path('<slug:slug>/delete/', TheaterDeleteView.as_view(), name='theater-delete'),
    path('<slug:slug>/restore/', TheaterRestoreView.as_view(), name='theater-restore'),

    # Nested Show Views (under a Theater)
    path('<slug:slug>/shows/', ShowListByTheaterView.as_view(), name='show-list-by-theater'),
    path('<slug:slug>/shows/create/', ShowCreateUnderTheaterView.as_view(), name='show-create-under-theater'),

    # Individual Show Operations
    path('shows/<int:pk>/', ShowDetailView.as_view(), name='show-detail'),
    path('shows/<int:pk>/update/', ShowUpdateView.as_view(), name='show-update'),
    path('shows/<int:pk>/delete/', ShowDeleteView.as_view(), name='show-delete'),
    path('shows/<int:pk>/restore/', ShowRestoreView.as_view(), name='show-restore'),
]
