from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Author, Comment
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .serializers import PostSerializer

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
