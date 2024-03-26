from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, Podcast, NewsletterSubscriber


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile_picture', 'is_author', 'is_admin')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["topic","tags","country","likes", "author", "read_time"]

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'