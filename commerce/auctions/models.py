from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


MAX_BID_DIGITS = 9

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True, db_index=True)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):

    # TODO: think about/account for timezones (created_at, opens_at, closes_at)

    # Meta
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    created_at = models.DateTimeField(default=datetime.now)

    # Content
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    image_url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="listings")
    starting_bid = models.DecimalField(max_digits=MAX_BID_DIGITS, decimal_places=2)

    # Other
    opens_at = models.DateTimeField(default=datetime.now)
    closes_at = models.DateTimeField()
    users_watching = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=MAX_BID_DIGITS, decimal_places=2)
    time = models.DateTimeField(default=datetime.now)

    class Meta():
        get_latest_by = 'amount'

    def __str__(self):
        return f"{self.user} bids {self.amount} for {self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user} comment on {self.listing}"
