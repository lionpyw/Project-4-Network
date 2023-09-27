import json
import time
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Likes, User, Post, Profile
from .paginator import add_paginator



def index(request):
    return render(request, "network/index.html")

def view_posts(request):
    posts = Post.objects.all()
    serialized = [post.serialize() for post in posts]
    page_number = request.GET.get("page")
    pagez = add_paginator(serialized_data=serialized, p_number=page_number)
    time.sleep(1)
    return JsonResponse(pagez, safe=False)


def profile_page(request, person_id):
    user = Profile.objects.get(person=person_id)
    posts = Post.objects.filter(author_id=person_id)
    serialized = [post.serialize() for post in posts]
    page_number = request.GET.get("page")
    pagez = add_paginator(serialized_data=serialized, p_number=page_number)
        
    return JsonResponse([user.serialize(),pagez], safe=False)


def profile_image(request, person_id):
    user = Profile.objects.get(person=person_id)
    if request.method == 'POST':  
        image = request.FILES['image']
        user.image = image
        user.save()
        return JsonResponse({'imageUrl': user.image.url }, status=200)
    


@login_required
def follow(request, person_id):
    user = request.user
    profile = Profile.objects.get(person = user.id)
    fan = Profile.objects.get(person = person_id)
    nr=0
    for follower in profile.following.all():
        if fan.person_id == follower.person_id: # type: ignore
            profile.following.remove(person_id)
            profile.save()
            nr=1
            break
    if nr != 1:    
        profile.following.add(person_id)
        profile.save()
    
    return JsonResponse({"message": "Follow status successful."}
                        , status=200)

@login_required
def follow_posts(request):
    user = request.user
    profile = Profile.objects.get(person = user.id)
    following= profile.following.exclude(person = request.user).all()
    follow_list=[follow.person.id for follow in following]
    posts=Post.objects.filter(author_id__in=follow_list)
    serialized = [post.serialize() for post in posts]
    page_number = request.GET.get("page")
    pagez = add_paginator(serialized_data=serialized, p_number=page_number)
    return JsonResponse(pagez, safe=False)

@login_required
def post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    user = request.user
    body = data.get("body", "")
    post= Post.objects.create(author_id=user.id, post=body)
    Likes.objects.create(post_id=post.id) # type: ignore
    
    return JsonResponse({"message": "Post successfull!"}, status=201)

@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        comment = data.get("post", "")
        post.post = comment
        post.published = datetime.datetime.now # type: ignore
        post.save()
        return JsonResponse({"message": "Post edit successfull!"}, status=201)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def like(request, post_id):
    user = request.user
    id = user.id
    (liked,created) = Likes.objects.get_or_create(post_id=post_id)
    rem=0
    if liked.user.all().count() > 0:
        for person in liked.user.all():
            if id == person.person_id:
                liked.user.remove(id)
                liked.save()
                rem=1
                break
    if rem == 0:
        liked.user.add(id)
        liked.save()
    post = Post.objects.get(id=post_id)
    post_likes = post.likes.user.all().count() # type: ignore
    return JsonResponse(post.serialize(), status=200)
    


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
            user = User.objects.create_user(username, email, password) # type: ignore
            profile = Profile.objects.create(person=user)
            profile.following.set([user.id])
            profile.save()
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
