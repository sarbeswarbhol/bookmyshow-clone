from django.urls import path
from .views import (
    # Theater views
    TheaterListView, TheaterCreateView, TheaterDetailView, TheaterRestoreView,
    TheaterUpdateView, TheaterDeleteView,

    # Screen views
    ScreenListByTheaterView, ScreenCreateUnderTheaterView, ScreenDetailView,
    ScreenUpdateView, ScreenDeleteView, ScreenRestoreView,

    # Show views
    ShowListByTheaterView, ShowCreateUnderTheaterView, ShowDetailView,
    ShowUpdateView, ShowDeleteView, ShowRestoreView,
)

urlpatterns = [
    # 🎭 Theaters
    path('', TheaterListView.as_view(), name='theater-list'),
    path('create/', TheaterCreateView.as_view(), name='theater-create'),
    path('<slug:slug>/', TheaterDetailView.as_view(), name='theater-detail'),
    path('<slug:slug>/update/', TheaterUpdateView.as_view(), name='theater-update'),
    path('<slug:slug>/delete/', TheaterDeleteView.as_view(), name='theater-delete'),
    path('<slug:slug>/restore/', TheaterRestoreView.as_view(), name='theater-restore'),

    # 🖥️ Screens under Theater
    path('<slug:slug>/screens/', ScreenListByTheaterView.as_view(), name='screen-list-by-theater'),
    path('<slug:slug>/screens/create/', ScreenCreateUnderTheaterView.as_view(), name='screen-create-under-theater'),

    # 🖥️ Flat Screen operations
    path('screens/<int:pk>/', ScreenDetailView.as_view(), name='screen-detail'),
    path('screens/<int:pk>/update/', ScreenUpdateView.as_view(), name='screen-update'),
    path('screens/<int:pk>/delete/', ScreenDeleteView.as_view(), name='screen-delete'),
    path('screens/<int:pk>/restore/', ScreenRestoreView.as_view(), name='screen-restore'),

    # 🎬 Shows under Theater
    path('<slug:slug>/shows/', ShowListByTheaterView.as_view(), name='show-list-by-theater'),
    path('<slug:slug>/shows/create/', ShowCreateUnderTheaterView.as_view(), name='show-create-under-theater'),

    # 🎬 Flat Show operations
    path('shows/<int:pk>/', ShowDetailView.as_view(), name='show-detail'),
    path('shows/<int:pk>/update/', ShowUpdateView.as_view(), name='show-update'),
    path('shows/<int:pk>/delete/', ShowDeleteView.as_view(), name='show-delete'),
    path('shows/<int:pk>/restore/', ShowRestoreView.as_view(), name='show-restore'),
]
