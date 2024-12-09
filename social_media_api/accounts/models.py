from django.db import models

from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField()
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    
    
