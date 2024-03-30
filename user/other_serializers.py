# serializers.py
from rest_framework import serializers
from .models import Post, Podcast
from django.contrib.auth import get_user_model
from .main_serializers import  UserSerializer
User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'topic', 'tag', 'country', 'content', 'author')

    def create(self, validated_data):
        # Calculate read time based on content length (assuming average reading speed)
        content_length = len(validated_data['content'])
        read_time = content_length / 1000  # Assuming 1000 characters per minute reading speed
        validated_data['read_time'] = round(read_time)
        return super().create(validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'
