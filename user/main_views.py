from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Podcast, NewsletterSubscriber
from rest_framework.pagination import PageNumberPagination
from .main_serializers import PostSerializer, PodcastSerializer, NewsletterSubscriberSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .main_serializers import UserSerializer
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    serializer_class = MyTokenObtainPairSerializer

class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        try:
            # Validate the token
            refresh_token = request.data['refresh_token']

            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({e}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)



class HeroPostsAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()[:3]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class RecentPostsAPIView(APIView):
    def get(self, request):
        recent_posts = Post.objects.all().order_by('-created_at')[:6]  # Fetch six most recent posts
        serializer = PostSerializer(recent_posts, many=True)
        return Response(serializer.data)


class PopularPostsAPIView(APIView):
    def get(self, request):
        # Fetch three popular and trending posts (you may customize this logic based on your requirements)
        popular_posts = Post.objects.all().order_by('-likes')[:3]
        serializer = PostSerializer(popular_posts, many=True)
        return Response(serializer.data)

class TwoPodcastsPerPagePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PodcastListAPIView(APIView):
    def get(self, request):
        podcasts = Podcast.objects.all()
        paginator = TwoPodcastsPerPagePagination()
        result_page = paginator.paginate_queryset(podcasts, request)
        serializer = PodcastSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class SearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')  # Get the search query from the request
        query = query.lower()  # Convert query to lowercase for case insensitivity

        # Search posts and serialize the results
        posts = Post.objects.filter(Q(content__icontains=query) | Q(tags__icontains=query))
        post_serializer = PostSerializer(posts, many=True)

        # Paginate and serialize related podcasts
        related_podcasts = Podcast.objects.filter(Q(topic__icontains=query) | Q(host__icontains=query))
        paginator = TwoPodcastsPerPagePagination()
        result_page = paginator.paginate_queryset(related_podcasts, request)
        podcast_serializer = PodcastSerializer(result_page, many=True)

        # Return data in the specified format
        return Response({
            "posts": post_serializer.data,
            "related_podcasts": paginator.get_paginated_response(podcast_serializer.data).data
        })


class NewsletterSubscriptionAPIView(APIView):
    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email = request.data.get('email')
        if email:
            try:
                subscriber = NewsletterSubscriber.objects.get(email=email)
                subscriber.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except NewsletterSubscriber.DoesNotExist:
                return Response({'detail': 'Subscriber not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Email not provided.'}, status=status.HTTP_400_BAD_REQUEST)