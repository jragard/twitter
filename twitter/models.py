from django.db import models
from django.contrib.auth.models import User

class TwitterUser(models.Model):
    # Subclass of django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=12)
    following = models.ManyToManyField('self')

    def __str__(self):
        return self.username


class Tweet(models.Model):
    body = models.CharField(max_length=140)
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=25)

    def __str__(self):
        return self.body


class Notification(models.Model):
    pass

