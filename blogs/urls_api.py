from django.urls import path
from .views import PostListAPIView, PostRetrieveAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='api-post-list'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='api-post-detail'),
]
