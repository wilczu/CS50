from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listingID>", views.listing, name="listing"),
    path("watchlist/<int:userID>", views.watching, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("endlisting/<int:listingID>", views.end_listing, name="endListing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:categoryID>", views.category, name="category")
]
