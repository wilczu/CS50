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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category_name")
    image = models.CharField(max_length=128, default=None, blank=True)
    active = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.category} : {self.image}"

class UserListing(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default="none", related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="owner")

    def __str__(self):
        return f"{self.user.id}"

class watchlist(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watched")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")

    def __str__(self):
        return f"{self.listing.title} : {self.user.username}"

class bidding(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="biddingListing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddingUser")
    bid = models.DecimalField(max_digits=10000, decimal_places=2)

    def __str__(self):
        return f"{self.listing.title} : {self.user.username} : {self.bid}"

class comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commentedon")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comment = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title} said {self.comment}"
