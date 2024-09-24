from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Listing/<str:item>/", views.listing, name="listing"),
    path("Listing/<str:item>/Closed/", views.close_listing, name="close_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Add-<str:item>-To-Watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path("Remove-<str:item>-From-Watchlist/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("Categories/All/", views.all_categories, name="all_categories"),
    path("Categories/<str:category_name>/", views.category, name="category"),
    path("Watchlist/", views.watchlist, name="watchlist"),
    path("Create_Listing/", views.create_listing, name="create_listing"),
    path("Listings/Ended/", views.closed_listings, name="closed_listings")

]
