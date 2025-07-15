from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string

def unique_slugify(instance, value, slug_field_name='slug', queryset=None):
    slug = slugify(value)
    if queryset is None:
        queryset = instance.__class__.all_objects.all()
    
    orig_slug = slug

    while queryset.filter(**{slug_field_name: slug}).exists():
        slug = f"{orig_slug}-{get_random_string(4)}"

    return slug




class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Screen(models.Model):
    theater = models.ForeignKey(Theater, related_name='screens', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} at {self.theater.name}"

class Show(models.Model):
    screen = models.ForeignKey(Screen, related_name='shows', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', related_name='shows', on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.movie.title} at {self.screen.theater.name} on {self.show_time.strftime('%Y-%m-%d %H:%M')}"
