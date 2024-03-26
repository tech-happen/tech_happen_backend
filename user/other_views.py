# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post,Podcast
from .other_serializers import PostSerializer, PostDetailSerializer,PodcastSerializer

class PostCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)

class PodcastCreateAPIView(generics.CreateAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    permission_classes = (IsAuthenticated,)

