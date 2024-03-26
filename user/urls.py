# urls.py
from django.urls import path
from .main_views import HeroPostsAPIView, RecentPostsAPIView, PopularPostsAPIView,PodcastListAPIView, NewsletterSubscriptionAPIView,SearchAPIView
from .other_views import PostCreateAPIView, PostDetailAPIView, PodcastCreateAPIView

urlpatterns = [
    path('posts/', PostCreateAPIView.as_view(), name='post-lis-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('hero-posts/', HeroPostsAPIView.as_view(), name='hero-posts'),
    path('recent-posts/', RecentPostsAPIView.as_view(), name='recent-posts'),
    path('popular-posts/', PopularPostsAPIView.as_view(), name='popular-posts'),
    path('podcasts/', PodcastCreateAPIView.as_view(), name='podcast-create'),
    path('podcasts/', PodcastListAPIView.as_view(), name='podcast-list'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('newsletter/subscribe/', NewsletterSubscriptionAPIView.as_view(), name='subscribe-newsletter'),
    path('newsletter/unsubscribe/', NewsletterSubscriptionAPIView.as_view(), name='unsubscribe-newsletter'),
]
