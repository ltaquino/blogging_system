from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView,add_comment

app_name = 'blogs'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/add-comment/', add_comment, name='add-comment'),
]