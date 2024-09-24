from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.order_by('-date_created').all()
    })

def listing(request, item):
    listing = Listing.objects.get(title=item)
    cat = listing.category

    if request.method == "POST":
        if request.POST.get('bid') and float(request.POST.get('bid')) > float(listing.price):
            Bid.objects.create(
                listing = listing,
                created_by = request.user,
                amount = request.POST.get('bid')
            )
            listing.price = request.POST.get('bid')
            listing.num_bids += 1
            listing.save()
            messages.success(request, f"Successful bid of {listing.price} on the item '{listing.title}'")
            return redirect('listing', item=listing.title)
        elif request.POST.get('bid') and float(request.POST.get('bid')) <= float(listing.price):
            messages.error(request, 'Bid must be more than the current bid.')
        else:
            Comment.objects.create(
                listing = listing,
                created_by = request.user,
                body = request.POST.get('body')
            )
            messages.success(request, "Successfully created a comment.")
            return redirect('listing', item=listing.title)

    if listing.num_bids == 0:
        bid = None
    else:
        bid = Bid.objects.get(amount=listing.price, listing=listing)

    if not request.user.is_authenticated:
        user_watchlist = None
    else:
        user_watchlist = Watchlist.objects.get(associated_user=request.user).listings.all()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "others": Listing.objects.exclude(title=item).filter(category=cat).order_by('-num_bids')[0:3],
        "bid": bid,
        "comments": Comment.objects.filter(listing=listing),
        "user_watchlist": user_watchlist
    })

@login_required
def close_listing(request, item):
    listing = Listing.objects.get(title=item)

    if request.method == "POST":
        listing.is_active = False;
        listing.save()
        messages.success(request, f"Successfully closed the listing of '{listing.title}'.")

    return redirect('listing', item=listing.title)

@login_required
def add_to_watchlist(request, item):
    listing = Listing.objects.get(title=item)

    if request.method == "POST":
        watchlist = Watchlist.objects.get(associated_user=request.user)
        watchlist.listings.add(listing)
        watchlist.save()
        messages.success(request, f"Successfully added '{listing.title}' to your watchlist.")
    
    return redirect('listing', item=listing.title)

@login_required
def remove_from_watchlist(request, item):
    listing = Listing.objects.get(title=item)

    if request.method == "POST":
        watchlist = Watchlist.objects.get(associated_user=request.user)
        watchlist.listings.remove(listing)
        watchlist.save()
        messages.success(request, f"Successfully removed '{listing.title}' from your watchlist.")
    
    return redirect('listing', item=listing.title)

def all_categories(request):
    return render(request, "auctions/all_categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_name):
    category = Category.objects.get(name=category_name)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": category.listings.order_by('-date_created').all()
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.get(associated_user=request.user).listings.all()
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            messages.success(request, f"The listing '{listing.title}' was succesfully created.")
            return redirect('listing', item=listing.title)
        
    form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def closed_listings(request):
    return render(request, "auctions/ended_listings.html", {
        "listings": Listing.objects.filter(is_active=False)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Watchlist.objects.create(
                associated_user = user
            )
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
