from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Club(models.Model):
    club_name = models.CharField(max_length=30)
    club_description = models.TextField()
    club_location = models.CharField(max_length=30)
    club_url = models.URLField(default="")
    club_genre = models.CharField(default="", max_length=30)
    club_picture = models.ImageField(upload_to='club_pictures', default='club_pictures/default_club.png', blank=True)
    eighteen_plus = models.BooleanField(default=False)
    average_club_rating = models.FloatField(default=0.0, blank=True)
    club_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=datetime.now, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(default='default.jpg', upload_to='profile_pictures',blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True)  # storing users profile bio.
    clubs_subscibed = models.ManyToManyField(Club, blank=True)  # Storing the clubs users saved/added.
    is_club_owner = models.BooleanField(default=False)  # stores whether user manages any club or not.
    age = models.PositiveIntegerField(default=20)
    location = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=100, default="male")
    favourites = models.TextField(null=True)

    def __str__(self):
        return self.user.username
