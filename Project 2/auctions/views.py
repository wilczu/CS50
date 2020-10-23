from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max

from .models import *


def index(request):
    remove_sessions(request)

    return render(request, "auctions/index.html", {
        "Listings": Listings.objects.filter(active = 1).all()
    })


def remove_sessions(request):
    if 'error' in request.session:
        del request.session['error']
    if 'message' in request.session:
        del request.session['message']
    if 'comment_error' in request.session:
        del request.session['comment_error']


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

        request.session['message'] = True
        return redirect('create_listing')

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def get_highest_bid(listingID):
    listing = Listings.objects.get(pk=int(listingID))
    highest = bidding.objects.filter(listing=listing.id).last()
    #Return highest bid of there is one
    if bidding.objects.filter(listing=listing.id).count() > 0:
        return {'user':highest.user.username, 'bid':highest.bid}
    else:
        return {'user': None, 'bid': '00.00'}

def listing(request, listingID):

    listing = Listings.objects.get(pk=int(listingID))
    if request.user.is_authenticated:
        watching_now = watchlist.objects.filter(listing = listing, user = request.user)
        owner = UserListing.objects.filter(listing = listing, user = request.user).first()
    else:
        watching_now = None
        owner = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watching": watching_now,
        "highest_bid": get_highest_bid(listing.id)['bid'],
        "comments": comments.objects.filter(listing = listing),
        "owner": owner,
        "winner": get_highest_bid(listing.id)['user']
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


def bid(request):
    if request.method == "POST":

        listing = Listings.objects.get(pk=int(request.POST["listingID"]))
        user = User.objects.get(pk=int(request.user.id))

        placed_bid = round(float(request.POST["newBid"]), 2)

        placed_bid = round(float(request.POST["newBid"]), 2)
        highest_bid = get_highest_bid(listing.id)['bid']

        if placed_bid >= float(listing.start_bid) and placed_bid > float(highest_bid):
            save_bid = bidding.objects.create(
                listing = listing,
                user = user,
                bid = placed_bid
            )
            save_bid.save()

            remove_sessions(request)
        else:
            request.session['error'] = True

        return redirect('listing', listingID=listing.id)

def comment(request):
    if request.user.is_authenticated and request.method == "POST":
        comment = request.POST['comment']
        listing = Listings.objects.get(pk=int(request.POST['listingID']))
        user = User.objects.get(pk=int(request.user.id))

        if len(comment) >=1 and len(comment) <=512:
            save_comment = comments.objects.create(
                listing = listing,
                user = user,
                comment = comment
            )
            save_comment.save()

            return redirect('listing', listingID=listing.id)
        else:
            request.session['comment_error'] = True
            return redirect('listing', listingID=listing.id)

    else:
        return render(request, "auctions/index.html", {
            "Listings": Listings.objects.all()
        })


def end_listing(request, listingID):
    owner = UserListing.objects.filter(listing = listingID, user = request.user).first()
    #Check if user is owning this listing again
    if owner:
        listing = Listings.objects.get(pk=int(listingID))
        listing.active = 0
        listing.save()

    return redirect('listing', listingID=listingID)


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, categoryID):
    getCategory = Category.objects.get(pk=int(categoryID))
    return render(request, "auctions/category.html", {
        "Category": getCategory.name,
        "Listings": Listings.objects.filter(active = 1, category = getCategory).all()
    })
