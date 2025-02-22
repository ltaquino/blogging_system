from rest_framework import serializers
from .models import Author, Post, Comment

#task 1
class PostSerializer(serializers.ModelSerializer):
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
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value


#task4
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content','published_date']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if Post.objects.filter(title=value).exists():
            raise serializers.ValidationError("A post with this title already exists.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content should be at least 10 characters long.")
        return value


#task5
class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'active']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content should be at least 10 characters long.")
        return value