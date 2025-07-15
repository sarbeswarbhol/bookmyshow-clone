from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('theater_owner', 'Theater Owner'),
        ('movie_owner', 'Movie Owner'),
        ('admin', 'Admin'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
