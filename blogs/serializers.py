from rest_framework import serializers
from .models import Author, Post, Comment

class PostSerializer(serializers.ModelSerializer):
    #author = AuthorSerializer(read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author_name']

