from rest_framework import serializers
from .models import Author, Post, Comment

#task 1
class PostSerializer(serializers.ModelSerializer):
    #author = AuthorSerializer(read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author_name']

#task2
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created']

class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)  

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author_name', 'status', 'active', 'comments']

#task3
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


#task4
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content','published_date']


#task5
class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'active']