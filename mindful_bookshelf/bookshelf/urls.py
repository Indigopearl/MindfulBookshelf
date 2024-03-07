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
    path("add_category/", views.add_category, name="add_category"),
    # Add more URL patterns as needed
]
