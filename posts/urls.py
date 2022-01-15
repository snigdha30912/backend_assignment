from django.urls import path
from emailAuth.views import LoginAPIView
from .views import UserAPIView, FollowAPIView, UnfollowAPIView, PostsCreateAPIView, PostDetailAPIView, LikeAPIView, UnlikeAPIView, CommentsCreateAPIView, AllPostsAPIView

urlpatterns = [
    path('user', UserAPIView.as_view(), name="user"),
    path('follow/<int:pk>', FollowAPIView.as_view(), name="follow"),
    path('unfollow/<int:pk>', UnfollowAPIView.as_view(), name="unfollow"),
    path('posts/', PostsCreateAPIView.as_view(), name="posts"),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name="post-detail"),
    path('like/<int:pk>', LikeAPIView.as_view(), name="like"),
    path('unlike/<int:pk>', UnlikeAPIView.as_view(), name="unlike"),
    path('comment/<int:pk>', CommentsCreateAPIView.as_view(), name="comments"),
    path('all_posts/', AllPostsAPIView.as_view(), name="all-posts"),
    path('authenticate/', LoginAPIView.as_view(), name="login"),
]
