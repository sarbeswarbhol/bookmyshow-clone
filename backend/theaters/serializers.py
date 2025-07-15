from rest_framework import serializers
from .models import Theater, Screen, Show
from movies.serializers import MovieSerializer
from movies.models import Movie


# 🎭 Theater Serializer
class TheaterSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = ['id', 'name', 'location', 'slug', 'created_by']
        read_only_fields = ['slug', 'created_by']

    def get_created_by(self, obj):
        return obj.created_by.username


# 🖥️ Screen Serializer
class ScreenSerializer(serializers.ModelSerializer):
    theater = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Screen
        fields = ['id', 'name', 'slug', 'theater', 'created_by']
        read_only_fields = ['slug', 'created_by']


# 🎬 Show Serializer
class ShowSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.filter(is_deleted=False),
        source='movie',
        write_only=True
    )
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'screen', 'movie', 'movie_id', 'show_time', 'created_by']
        read_only_fields = ['created_by']

    def get_created_by(self, obj):
        return obj.created_by.username
