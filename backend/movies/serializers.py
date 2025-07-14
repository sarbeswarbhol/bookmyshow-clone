from rest_framework import serializers
from .models import Movie, CastMember, Review




class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = ['id', 'name', 'role', 'profile_picture']


class MovieSerializer(serializers.ModelSerializer):
    cast = CastMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'description', 'language', 'genre',
            'duration', 'rating', 'cast', 'release_date', 'poster'
        ]


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
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = [
            'id', 'movie', 'user', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['user', 'movie', 'created_at']



class CastMemberDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = CastMember
        fields = ['id', 'name', 'role', 'profile_picture', 'movies']