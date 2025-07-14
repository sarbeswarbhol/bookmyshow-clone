from rest_framework import serializers
from .models import Theater, Show
from movies.serializers import MovieSerializer
from movies.models import Movie
 

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'location', 'capacity', 'slug', 'created_by']
        read_only_fields = ['slug', 'created_by']

class ShowSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.filter(is_deleted=False),
        source='movie',
        write_only=True
    )

    class Meta:
        model = Show
        fields = ['id', 'theater', 'movie', 'movie_id', 'show_time', 'created_by']
        read_only_fields = ['theater', 'created_by']

