from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username}"

class Profile(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    following = models.ManyToManyField('self',blank=True,related_name='followers',symmetrical=False)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='network/images',default='dafault.jpg')
    about = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.person.username}"
    
    
    def serialize(self):
        follower_list= []
        follower_list_ids = []
        for follower in self.followers.all():
            if self.person.username != follower.person.username:
                follower_list.append(follower.person.username)
                follower_list_ids.append(follower.person_id)
        following_list = [following.person.username for following in self.following.all()
                          if self.person.username != following.person.username]
        
        
        return {
            "user" : self.person.username,
            "user_id" : self.person_id,
            "following"  : following_list,
            "nr_following" : len(following_list),
            "followers" : follower_list,
            "nr_follower" : len(follower_list),
            "follower_id" : follower_list_ids,
            "image" : self.image.url,
            "about" : self.about
        }
        


class Post(models.Model):
    post = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="author")
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author} on {self.published}'
    
    def serialize(self):
        return {
            "id" : self.id, 
            "post" : self.post,
            "author" : self.author.person.username,
            "author_pic": self.author.person.profile.image.url,
            "author_id"  : self.author_id, 
            "timestamp" : self.published.strftime("%b %d %Y, %I:%M %p"),
            "likes" : self.likes.user.all().count() 
        }    
    class Meta:
        ordering = ['-published']

    

class Likes(models.Model):
    user = models.ManyToManyField(Profile, related_name="liked", blank=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes', primary_key=True)

    def serialize(self):
        return {
            "post" : self.post_id 
        }

    def __str__(self):
        return f"{self.post.id} has {self.user.all().count()} likes"


