from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Author
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404

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