from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    proflie_image = models.ImageField(upload_to="media", default="avatar.jpg")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user.username)


class Post(BaseModel):
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_image")
    caption = models.TextField(blank=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Like(BaseModel):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Followers_Model(BaseModel):
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class Chat(BaseModel):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reciever")
    msg = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender.user.username)

    class Meta:
        ordering = ["is_read", "-created"]
