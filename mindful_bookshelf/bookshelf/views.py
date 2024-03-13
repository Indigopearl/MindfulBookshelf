# bookshelf/views.py

from django.shortcuts import render, redirect, get_object_or_404
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
    book = get_object_or_404(Book, id=book_id)
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
        "categories": categories,
        # Add book_id for each book
        "book_details": [{"book": book, "book_id": book.id} for book in books],
    }

    return render(request, "bookshelf/admin_overview.html", context)


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("admin_overview")
    return redirect("admin_overview")


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


def user_details(request):
    if request.method == "GET":
        user_id = request.GET.get("id")
        user = User.objects.filter(id=user_id).first()
        if user:
            return render(request, "bookshelf/user_details.html", {"user": user})
        else:
            return render(request, "user_not_found.html")
    else:
        return HttpResponseNotAllowed(["GET"])


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("book_list")  # Redirect to book list page after adding book
    else:
        form = BookForm()
    return render(request, "bookshelf/add_book.html", {"form": form})


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


# Define a view function to edit a book
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/edit_book.html", {"form": form, "book": book})


# Define a view function to provide a book detail view
def book_detail(request, book_id=None):
    if book_id:
        book = get_object_or_404(Book, id=book_id)
    else:
        # Handle case where no book_id is provided (optional)
        book = None
    return render(request, "bookshelf/book_detail.html", {"book": book})


# Define a view function to mark a book as read
def mark_book_as_read(request, book_id):
    if request.method == "POST":
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        reading_status, created = ReadingStatus.objects.get_or_create(
            user=user, book=book
        )
        reading_status.read = True
        reading_status.save()
        return redirect("book_detail", book_id=book_id)
    else:
        return HttpResponseNotAllowed(["POST"])


def toggle_book_availability(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        if book_id:
            try:
                book = Book.objects.get(pk=book_id)
                book.available = not book.available
                book.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Book availability toggled successfully.",
                    }
                )
            except Book.DoesNotExist:
                return JsonResponse({"success": False, "message": "Book not found."})
    return JsonResponse(
        {"success": False, "message": "Invalid request method or missing parameters."}
    )
