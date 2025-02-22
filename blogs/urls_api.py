from django.urls import path
from .views import PostListAPIView, PostRetrieveAPIView, CommentCreateAPIView,PostCreateAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='api-post-list'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name='api-post-detail'),
    path('posts/<int:post_pk>/comments/', CommentCreateAPIView.as_view(), name='api-comment-create'),
    path('posts/create/', PostCreateAPIView.as_view(), name='api-post-create'),
]
