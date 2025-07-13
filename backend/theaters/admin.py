from django.contrib import admin
from .models import Show, Theater



@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'show_time', 'ticket_price', 'created_by')
    list_filter = ('show_time', 'theater', 'movie')
    search_fields = ('movie__title', 'theater__name')


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'created_by')
    search_fields = ('name', 'location')