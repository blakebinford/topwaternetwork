from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user_relation = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Needed for fishing Guides
    service_name = models.CharField(max_length=125, default='')
    is_guide = models.BooleanField(default=False)
    fish_location = models.CharField(max_length=80)
    service_location = models.CharField(max_length=80, default='')
    user_bio = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return '{}'.format(self.user_relation)
