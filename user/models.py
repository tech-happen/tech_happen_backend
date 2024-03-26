from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_author = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Post(models.Model):
    topic = models.CharField(max_length=100,)
    tags = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    content = models.TextField()
    read_time = models.IntegerField()  # In minutes


class Podcast(models.Model):
    topic = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    guests = models.CharField(max_length=255)  # Assuming multiple guests separated by comma
    audio_file = models.FileField(upload_to='podcasts/')
    length = models.IntegerField()  # In seconds

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
