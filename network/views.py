import json
import time
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models.aggregates import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from .serializers import ProfileSerializer, PostSerializer, LikesSerializer
from .models import Likes, Post, Profile
from .paginator import add_paginator

User = get_user_model()

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related('liked').select_related('person')\
        .prefetch_related("following").prefetch_related("followers")\
        .annotate(
        following_count = Count('following'),
        followers_count = Count('followers')
        ).all().order_by('-created')
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsAdminUser()]
        if self.request.method in ['PUT','PATCH']:
            return [IsAuthenticated()]
        return [AllowAny()]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author__person').select_related('likes')\
        .prefetch_related("likes__user").select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.prefetch_related("user").all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
        user.image.delete()
        user.image = image
        user.save()
        return JsonResponse({'imageUrl': user.image.url }, status=200)
    


@login_required
def follow(request, person_id):
    user = request.user
    profile = Profile.objects.get(person = user.id)
    fan = Profile.objects.get(person = person_id)

    if fan.person_id in [f.person_id for f in profile.following.all()]:
        profile.following.remove(person_id)
        profile.save()
    else:
        profile.following.add(person_id)
        profile.save()
    return JsonResponse({"message": "Follow status change successful."}
                        , status=200)

@login_required
def follow_posts(request):
    user = request.user
    profile = Profile.objects.get(person = user.id)
    following= profile.following.all()
    follow_list=[follow.person.id for follow in following]
    follow_list.append(user.id)
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
    Likes.objects.create(post_id=post.id)
    
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
        post.published = datetime.datetime.now
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
    (liked,_) = Likes.objects.get_or_create(post_id=post_id)
    
    if id in [person.person_id for person in liked.user.all()]:
        liked.user.remove(id)
        liked.save()
    else:
        liked.user.add(id)
        liked.save()
    post = Post.objects.get(id=post_id)
    post_likes = post.likes.user.all().count()
    return JsonResponse(post.serialize(), status=200)
    
