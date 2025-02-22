from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Author

from django.shortcuts import render

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

class PostCreateView(CreateView):
    model = Post
    template_name = 'templates/post_form.html'
    fields = ['title', 'content', 'author', 'status', 'active']
    success_url = reverse_lazy('blogs:post-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context