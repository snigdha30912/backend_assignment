from django.db import models
from emailAuth.models import User
from django.utils.timezone import now

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_desc = models.TextField(max_length=1200)
    created_at = models.DateTimeField(default=now)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.TextField(max_length=600)
    desc = models.TextField(max_length=1200)
    created_at = models.DateTimeField(default=now)
    likes = models.ManyToManyField("emailAuth.User", related_name="all_likes", blank=True)
    comments = models.ManyToManyField(Comment, default=[])
