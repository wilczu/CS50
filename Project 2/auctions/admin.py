from django.contrib import admin
from .models import User, Category, Listings, watchlist, bidding, comments
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(comments)
admin.site.register(watchlist)
admin.site.register(bidding)
