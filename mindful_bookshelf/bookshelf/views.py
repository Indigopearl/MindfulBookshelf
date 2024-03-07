from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm
from .forms import CategoryForm
from .models import Category


def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "bookshelf/book_detail.html", {"book": book})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "bookshelf/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "bookshelf/login.html",
                {"error_message": "Invalid username or password"},
            )
    else:
        return render(request, "bookshelf/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def admin_overview(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_overview")
    else:
        form = BookForm()

    # Query for books, users, and categories
    books = Book.objects.all()
    users = User.objects.exclude(is_superuser=True)
    categories = Category.objects.all()  # Query for categories

    # Pass data to the template
    context = {
        "form": form,
        "books": books,
        "users": users,
        "categories": categories,  # Pass categories to the template context
    }

    return render(request, "bookshelf/admin_overview.html", context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    if user_id != request.user.id:
        try:
            user_to_delete = User.objects.get(pk=user_id)
            user_to_delete.delete()
            return redirect("admin_overview")
        except User.DoesNotExist:
            # Handle case where user doesn't exist
            return render(
                request, "bookshelf/error.html", {"message": "User not found"}
            )
    else:
        return HttpResponseForbidden("You cannot delete yourself.")


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_overview")
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = CategoryForm()

    return render(request, "bookshelf/add_category.html", {"form": form})
