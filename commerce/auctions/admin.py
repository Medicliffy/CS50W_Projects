from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment

# Register your models here.
for model in [User, Category, Listing, Bid, Comment]:
    admin.site.register(model)