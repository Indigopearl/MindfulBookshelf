from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    # Add more URL patterns as needed
]
