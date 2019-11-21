from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True,on_delete=models.CASCADE)
    like_sth = models.CharField(max_length=1000, blank=True)
    dislike_sth = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)

class UserAndMovie(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    movie_id = models.CharField(max_length=100, blank=True, null=True)

