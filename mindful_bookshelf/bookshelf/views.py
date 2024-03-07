from django.shortcuts import render
from .models import Book


def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "bookshelf/book_detail.html", {"book": book})
