from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Post, Podcast, NewsletterSubscriber
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.settings import api_settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','profile_picture','is_admin', 'first_name', 'last_name', 'email' )
        extra_kwargs = {'password': {'write_only': True}, 'is_admin': {'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializerWithToken(UserSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']



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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data