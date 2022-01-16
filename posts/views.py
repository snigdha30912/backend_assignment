from django.shortcuts import render
from rest_framework import generics,status,permissions
from rest_framework.views import APIView
from emailAuth.models import User
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
from .permissions import IsOwner

class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, format=None):
        active_user = self.request.user
        user_data = {
            'username':active_user.username,
            'number_of_followers':active_user.followers.count(),
            'number_of_followings':active_user.followings.count(),
        }
        return Response(user_data,status.HTTP_200_OK)

class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request, pk, format=None):
        active_user = self.request.user
        try:
            target_user = User.objects.get(id=pk)
        except:
            return Response({"This user does not exist"},status.HTTP_404_NOT_FOUND)
        if active_user in target_user.followers.all():
            return Response({"You already follow this user"},status.HTTP_400_BAD_REQUEST)
        target_user.followers.add(active_user.id)
        active_user.followings.add(target_user.id)
        return Response({"You now follow this user"},status.HTTP_200_OK)

class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request, pk, format=None):
        active_user = self.request.user
        try:
            target_user = User.objects.get(id=pk)
        except:
            return Response({"This user does not exist"},status.HTTP_404_NOT_FOUND)
        if active_user not in target_user.followers.all():
            return Response({"You already don't follow this user."},status.HTTP_400_BAD_REQUEST)
        target_user.followers.remove(active_user.id)
        active_user.followings.remove(target_user.id)
        return Response({"You've unfollowed this user"},status.HTTP_200_OK)

class PostsCreateAPIView(generics.CreateAPIView):
    serializer_class=PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, serializer):
        serializer=PostSerializer(data = self.request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Post.objects.all()
    lookup_field = 'pk'
    def get(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        post_data = {
            'id':post.id,
            'number_of_likes':post.likes.count(),
            'number_of_comments':post.comments.count()
        }
        return Response(post_data, status.HTTP_200_OK)

class LikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request, pk, format=None):
        current_user = self.request.user
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"This post does not exist"},status.HTTP_404_NOT_FOUND)
        if current_user in post.likes.all():
            return Response({"You have already liked this post"},status.HTTP_400_BAD_REQUEST)
        post.likes.add(current_user.id)
        return Response({"You have liked this post"},status.HTTP_200_OK)

class UnlikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request, pk, format=None):
        current_user = self.request.user
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"This post does not exist"},status.HTTP_404_NOT_FOUND)
        if current_user not in post.likes.all():
            return Response({"You already don't like this post"},status.HTTP_400_BAD_REQUEST)
        post.likes.remove(current_user.id)
        return Response({"You unliked this post"},status.HTTP_200_OK)

class CommentsCreateAPIView(generics.CreateAPIView):
    serializer_class=CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        comment = serializer=CommentSerializer(data = self.request.data)
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"Post does not exist"},status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            comment = serializer.save(user=self.request.user)
            post.comments.add(comment)
            return Response(serializer.data,status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class AllPostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Post.objects.all().filter(user=self.request.user).order_by("created_at")
    
