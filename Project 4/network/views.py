from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts


def index(request):
    if request.method == "POST":
        content = request.POST['post_content']
        #Check if correct lenght
        if len(content) >= 1 and len(content) <= 2000:
            #Adding post to the database
            add_post = Posts.objects.create(
                post_owner = request.user,
                post_content = content
            )
            add_post.save()

            #Redirecting user to the main page after adding the post
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/index.html', {
                "all_posts": Posts.objects.all().order_by('-post_date'),
                "message": 'Your post has to have content and be no longer than 2000 characters'
            })

    return render(request, "network/index.html", {
        "all_posts": Posts.objects.all().order_by('-post_date')
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profil(request, userID):
    #Check if this user exists                                                          DONE
    #Get the data about this user                                                       DONE
    #Generate website with this user                                                    DONE
    #Get all posts made by this user
    #Check if this user is himself then do not display follow or unfollow button        DONE
    try:
        get_user = User.objects.get(pk=int(userID))
    except ObjectDoesNotExist:
        return HttpResponse("User not found!")

    return render(request, 'network/profil.html', {
        'user_nickname': get_user.username,
        'user_followers': get_user.followers,
        'user_following': get_user.following,
        'user_joined': get_user.date_joined,
        'user_seen': get_user.last_login,
        'user_posts': Posts.objects.all().filter(post_owner = get_user)
    })