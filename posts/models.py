from django.db import models
from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)
    content = models.TextField(max_length=1000, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.user.username) + "-post/" + str(self.pk)


class PostFiles(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    files = models.FileField(upload_to='post_files/', null=True, blank=True)

    def __str__(self):
        return str(self.post.user.username) + "-files/" + str(self.pk)

