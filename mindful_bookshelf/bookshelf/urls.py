# bookshelf/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("admin/overview/", views.admin_overview, name="admin_overview"),
    path(
        "admin/overview/delete_user/<int:user_id>/",
        views.delete_user,
        name="delete_user",
    ),
    path("add_book/", views.add_book, name="add_book"),
    path("add_category/", views.add_category, name="add_category"),
    path("book_detail/<int:book_id>/", views.book_detail, name="book_detail"),
    path("delete_book/", views.delete_book, name="delete_book"),
    path("edit/<int:book_id>/", views.edit_book_view, name="edit_book"),
    path("user-details/", views.user_details, name="user_details"),
    path(
        "toggle-book-availability/",
        views.toggle_book_availability,
        name="toggle_book_availability",
    ),
    # Add more URL patterns as needed
]
