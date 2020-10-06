from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, UserListing


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]

        # Saving the listing to the listings table
        new_listing = Listings.objects.create(
            title = title,
            description = request.POST["description"],
            start_bid = request.POST["starting_bid"],
            category = Category.objects.get(pk=int(request.POST["category"])),
            image = request.POST["image"]
        )
        new_listing.save()

        # Saving the listing ID and the user ID to the UserListing table
        link_user = UserListing.objects.create(
            listing = new_listing,
            user = User.objects.get(pk=request.POST["userID"])
        )
        link_user.save()

        return render(request, "auctions/create_listing.html", {
            "message": f"{title} was added to the shop!"
        })

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })
