from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False)
    profile_image = models.CharField(max_length=300)
    thumbnail_image = models.CharField(max_length=300)
    birthday = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)