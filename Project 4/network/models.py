from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


class Posts(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner")
    post_content = models.CharField(max_length=2000)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.post_owner}"


class Follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_follows')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed')

    def __str__(self):
        return f"{self.target}"


class Likes(models.Model):
    who_liked = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.who_liked}"