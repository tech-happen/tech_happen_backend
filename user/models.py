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
    likes = models.IntegerField(default=0)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    read_time = models.IntegerField()  # In minutes

    def save(self, *args, **kwargs):
        # Calculate read time based on content
        words_per_minute = 200  # Average reading speed
        word_count = len(self.content.split())
        self.read_time = max(1, int(word_count / words_per_minute))  # Ensure read time is at least 1 minute
        super().save(*args, **kwargs)


class Podcast(models.Model):
    topic = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    guests = models.CharField(max_length=255)  # Assuming multiple guests separated by comma
    audio_file = models.FileField(upload_to='podcasts/')
    length = models.IntegerField()  # In seconds

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
