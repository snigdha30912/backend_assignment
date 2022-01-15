from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    comment_desc = serializers.CharField(write_only = True)
    class Meta:
        model = Comment
        fields = ['id', 'comment_desc']


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='comment_desc')
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at', 'comments', 'likes']




