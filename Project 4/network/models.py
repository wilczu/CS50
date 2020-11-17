from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    user_id = models.ForeignKey(User, on_delete= models.CASCADE, related_name="post_owner")
    post_content = models.CharField(max_length=2000)
    post_date = models.DateTimeField()

    def __str__(self):
        return f"{self.post_content} {self.post_date}"