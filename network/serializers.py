from rest_framework import serializers
from .models import Likes, Post, Profile
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = get_user_model()
        fields = ['id','username','email','first_name','last_name']

class ProfileSerializer(serializers.ModelSerializer):
    person = UserSerializer(read_only=True)
    followers_count = serializers.IntegerField(read_only = True)
    following_count= serializers.IntegerField(read_only = True)

    class Meta:
        model=Profile
        fields = ['person', 'following', 'followers','following_count','followers_count', 'created', 'image', 'liked']
        read_only_fields = ['person','following_count','followers_count','liked', 'created']

class BasicProfileSerializer(serializers.ModelSerializer):
    person = UserSerializer()
    class Meta:
        model = Profile
        fields = ['person', 'image']

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    author = BasicProfileSerializer(read_only=True)
    likes = LikesSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ['id','post', 'author', 'published', 'likes']

