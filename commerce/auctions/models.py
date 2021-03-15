from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

from datetime import datetime


Max_bid_digits = 9

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True, db_index=True)
    # description = models.TextField() # TODO: maybe delete?


class Listing(models.Model):
    
    # Meta
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    # TODO: account for timezones
    created_at = models.DateTimeField(default=datetime.now)
    auction_opens_at = models.DateTimeField(default=datetime.now)
    auction_closes_at = models.DateTimeField()
    
    # About
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings")
    # TODO: move to bid class?...probably not
    starting_bid = models.DecimalField(max_digits=Max_bid_digits, decimal_places=2)
    
    users_watching = models.ManyToManyField(User, blank=True, related_name="watchlist")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=Max_bid_digits, decimal_places=2)
    time = models.DateTimeField(default=datetime.now)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()