from django.db import models
from django.contrib.auth.models import  User
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL

# Create your models here.

# class User(AbstractUser):
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    avater = models.ImageField(null=True,upload_to='user/avater', default='user/avater.png')
    bio = models.TextField(null=True, blank=True)
    def __str__(self):
        if self.nickname:
            return f'{self.nickname}'
        else:
            return f'{self.user}'
       

class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    friends = models.ForeignKey(User, on_delete=CASCADE, related_name='friends')
    def __str__(self):
        return f'{self.user} <--> {self.friends}'



class Messages(models.Model):
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='MessFile/file', null=True, blank=True)
    image = models.ImageField(upload_to='MessFile/image', null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=CASCADE)
    bitween = models.ForeignKey(UserFriend , on_delete=CASCADE)
    def __str__(self):
        return f'{self.text}' 
