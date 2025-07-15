from django.db import models
from django.conf import settings

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
            self.slug = self.name.lower().replace(' ', '-')
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
            self.slug = self.name.lower().replace(' ', '-')
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
        return f"{self.movie.title} at {self.theater.name} on {self.show_time.strftime('%Y-%m-%d %H:%M')}"
