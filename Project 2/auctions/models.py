from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    start_bid = models.DecimalField(max_digits=10000, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="none", related_name="category_name")
    image = models.CharField(max_length=128, default="none")

    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.category} : {self.image}"

class UserListing(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="none", related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="owner")

    def __str__(self):
        return f"{self.listing_ID} : {self.user}"
