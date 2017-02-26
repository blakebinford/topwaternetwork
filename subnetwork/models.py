from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SubNetwork(models.Model):
    sub_name = models.CharField(max_length=40)
    followers = models.ManyToManyField(User)

    def __str__(self):
        return self.sub_name

    def number_of_followers(self):
        self.number = self.followers.count()
        return self.number

    def number_of_posts(self):
        self.total_posts = self.fishingreport_set.count()
        return self.total_posts
