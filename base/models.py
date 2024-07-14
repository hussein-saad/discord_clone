from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(default='no bio...',null=True)
    avatar = models.ImageField(null=True,default='avatar.svg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    



class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    host = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    topic = models.ForeignKey(Topic,null=True,on_delete=models.SET_NULL)
    participants = models.ManyToManyField(User, related_name='participants')
    
    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.name

class Message(models.Model):
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at', '-updated_at']
    
    
    def __str__(self):
        return self.body[0:50]