from django.db import models
from django.conf import settings
from functools import partial
from .utils import upload_file_with_timestamp

# Create partials with specific folders
cast_upload_path = partial(upload_file_with_timestamp, folder='cast_profiles/')
movie_upload_path = partial(upload_file_with_timestamp, folder='movie_posters/')
 
 
# All CastMember, Movie, and Review models will use these managers

class CastMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class MovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class ReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# Models for the movie application

class CastMember(models.Model):
    CAST_ROLE_CHOICES = [
    ('actor', 'Actor'),
    ('actress', 'Actress'),
    ('director', 'Director'),
    ('producer', 'Producer'),
    ('writer', 'Writer'),
    ('cinematographer', 'Cinematographer'),
    ('editor', 'Editor'),
    ('composer', 'Composer'),
    ('music_director', 'Music Director'),
    ('choreographer', 'Choreographer'),
    ('art_director', 'Art Director'),
    ('costume_designer', 'Costume Designer'),
    ('makeup_artist', 'Makeup Artist'),
    ('stunt_coordinator', 'Stunt Coordinator'),
    ('voice_actor', 'Voice Actor'),
]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=CAST_ROLE_CHOICES)
    profile_picture = models.ImageField(
        upload_to=cast_upload_path,
        blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)

    objects = CastMemberManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.role})"

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.ManyToManyField(CastMember, related_name='movies')
    release_date = models.DateField()
    poster = models.ImageField(
        upload_to=movie_upload_path,
        blank=True, null=True
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = MovieManager()
    all_objects = models.Manager() 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_deleted = models.BooleanField(default=False)

    objects = ReviewManager()
    all_objects = models.Manager()

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}★)"