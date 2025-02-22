from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Author, Comment
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics,permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import PostSerializer,PostDetailSerializer,CommentCreateSerializer,PostCreateSerializer
from django.utils import timezone

class PostListView(ListView):
    model = Post
    template_name = 'templates/post_list.html'  
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
       return Post.objects.select_related('author').all() 

class PostDetailView(DetailView):
    model = Post
    template_name = 'templates/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class PostCreateView(CreateView):
    model = Post
    template_name = 'templates/post_form.html'
    fields = ['title', 'content', 'author', 'status', 'active']
    success_url = reverse_lazy('blogs:post-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
    return redirect('blogs:post-detail', pk=post.pk)


#2. REST API with Django REST Framework

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.filter(active=True).select_related('author')
        request = self.request
        title = request.query_params.get('title')
        author_name = request.query_params.get('author_name')
        published_date = request.query_params.get('published_date')

        if title:
            qs = qs.filter(title__icontains=title)
        if author_name:
            qs = qs.filter(author__name__icontains=author_name)
        if published_date:
            qs = qs.filter(published_date__date=published_date)
        
        return qs


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostDetailSerializer


#task3
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        
        if not post.active:
            raise ValidationError("Cannot add comment to an inactive post.")
        
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(post=post, user=user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as exc:
            return Response({'detail': exc.detail}, status=status.HTTP_400_BAD_REQUEST)


#task 4
class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            raise ValidationError("You are not registered as an author and cannot create posts.")
        
        serializer.save(author=author, active=True)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Post created successfully!", "data": response.data},
            status=status.HTTP_201_CREATED
        )