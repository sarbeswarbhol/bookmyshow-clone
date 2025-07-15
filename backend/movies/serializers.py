from rest_framework import serializers
from .models import Movie, CastMember, Review




class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = ['id', 'name', 'role', 'profile_picture']


class MovieSerializer(serializers.ModelSerializer):
    cast = CastMemberSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'description', 'language', 'genre',
            'duration', 'rating', 'cast', 'release_date', 'poster',
            'created_by'
        ]
        read_only_fields = ['slug', 'created_by_id', 'created_by_username']


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'language', 'genre',
            'duration', 'rating', 'cast', 'release_date', 'poster'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    

class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'movie_id',
            'movie_title',
            'user_id',
            'username',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = ['user_id', 'username', 'movie_id', 'movie_title', 'created_at']


class CastMemberDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = CastMember
        fields = ['id', 'name', 'role', 'profile_picture', 'movies']