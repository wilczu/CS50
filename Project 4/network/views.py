from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import F

from .models import User, Posts, Follows


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
    try:
        get_user = User.objects.get(pk=int(userID))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>User not found</h1>')
    
    follower = User.objects.get(pk=int(request.user.id))
    follow_object = Follows.objects.filter(follower = follower).filter(target = get_user)

    if follow_object:
        is_following = True
    else:
        is_following = False

    if request.method == "POST":
        action = request.POST['action']
        #Check if this user is already following the target
        if action == 'follow' and is_following == False:
            #Add follower and target to the follows table
            follow_user = Follows.objects.create(
                follower = follower,
                target = get_user
            )     
            follow_user.save()
            #Increment the number of following (user)
            User.objects.filter(pk=int(request.user.id)).update(following=F("following") +1)
            #Increment the number of followers (target)
            User.objects.filter(pk=int(userID)).update(followers=F("followers") +1)

            return redirect('profil', userID)
        elif action == 'unfollow' and is_following == True:
            #Removing follower and target users from the table
            follow_object.delete()
            #Remove one from following (user)
            User.objects.filter(pk=int(request.user.id)).update(following=F("following") -1)
            #Remove one from followers (target)
            User.objects.filter(pk=int(userID)).update(followers=F("followers") -1)
            return redirect('profil', userID)
        else:
            return redirect('profil', userID)

    return render(request, 'network/profil.html', {
        'user_id': get_user.id,
        'user_nickname': get_user.username,
        'user_followers': get_user.followers,
        'user_following': get_user.following,
        'user_joined': get_user.date_joined,
        'user_seen': get_user.last_login,
        'user_posts': Posts.objects.all().filter(post_owner = get_user).order_by('-post_date'),
        "follow_status": is_following 
    })


def following(request):
    if request.user.is_authenticated:
        followed_people = Follows.objects.filter(follower=request.user).values('target')
        return render(request, 'network/following.html', {
            "followers_posts": Posts.objects.filter(post_owner__in = followed_people) 
        })
    else:
        return redirect('index')