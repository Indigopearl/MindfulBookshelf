from django.contrib import admin
from django.urls import path, include
from bookshelf import views

urlpatterns = [
    path("", views.book_list, name="home"),  # Redirect root URL to book list view
    path("admin/", admin.site.urls),
    path("bookshelf/", include("bookshelf.urls")),
    # Add more URL patterns as needed
]
