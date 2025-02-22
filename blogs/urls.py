from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'blogs'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
]