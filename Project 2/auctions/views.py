from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listings, UserListing, watchlist


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
        image = request.POST["image"]
        category = request.POST["category"]

        if not image:
            image = "none"
        if category == '0':
            new_listing = Listings.objects.create(
                title = title,
                description = request.POST["description"],
                start_bid = request.POST["starting_bid"],
                image = image
            )
        else:
            new_listing = Listings.objects.create(
                title = title,
                description = request.POST["description"],
                start_bid = request.POST["starting_bid"],
                category = Category.objects.get(pk=int(request.POST["category"])),
                image = image
            )

        # Saving the listing to the listings table
        new_listing.save()

        # Saving the listing ID and the user ID to the UserListing table
        link_user = UserListing.objects.create(
            listing = new_listing,
            user = request.user
        )
        link_user.save()

        return render(request, "auctions/listing.html", {
            "message": f"{title} was added to the shop!"
        })

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def listing(request, listingID):
    listing = Listings.objects.get(pk=int(listingID))
    if request.user.is_authenticated:
        watching_now = watchlist.objects.filter(listing = listing, user = request.user)
    else:
        watching_now = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watching": watching_now
    })


def watching(request, userID):
    if request.method == "POST":
        action = request.POST["action"]
        product = Listings.objects.get(pk=int(request.POST["listing"]))
        #execute when user is adding item to the watchlist
        if action == "add":
            add = watchlist.objects.create(
                listing = product,
                user = request.user
            )
            add.save()
            return redirect('listing', listingID=product.id)

        #execute when user is removing item from the watchlist
        elif action == "remove":
            remove_me = watchlist.objects.get(listing = product, user = request.user)
            remove_me.delete()
            return redirect('listing', listingID=product.id)

    return render(request, "auctions/watchlist.html", {
        "watchItems": watchlist.objects.filter(user=int(userID))
    })
