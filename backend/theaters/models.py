from django.db import models
from django.conf import settings

class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Show(models.Model):
    theater = models.ForeignKey(Theater, related_name='shows', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', related_name='shows', on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} on {self.show_time.strftime('%Y-%m-%d %H:%M')}"