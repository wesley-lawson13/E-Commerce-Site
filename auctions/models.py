from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=350)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=350)
    image = models.ImageField(upload_to="auctions/images/", blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    num_bids = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} selling for ${self.price}"

class Watchlist(models.Model):
    associated_user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True, null=True)

    def __str__(self):
        return f"{self.associated_user.username}'s watchlist was created"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.created_by} placed a bid of {self.amount} on {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.created_by} commented on {self.listing.title}"