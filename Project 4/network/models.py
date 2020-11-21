from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


class Posts(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.CharField(max_length=2000)
    post_likes = models.IntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_owner} {self.post_content} {self.post_date}"


class Follows(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_follows')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed')

    def __str__(self):
        return f"{self.target} : {self.follower}"