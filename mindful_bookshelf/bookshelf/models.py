# bookshelf/models.py


from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django import forms


# Define your Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Define your Book model
class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    publication_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover_image = models.ImageField(
        upload_to="static/bookshelf/book/img/", blank=True, null=True
    )
    pdf_document = models.FileField(
        upload_to="static/bookshelf/books/pdf/", blank=True, null=True
    )

    def __str__(self):
        return self.title


# Define your ReadingStatus model
class ReadingStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {'Read' if self.read else 'Unread'}"


# Define your ReadingHistory model
class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.read_date}"


# Define your BookForm
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


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


# Define a view function to provide a book list view
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


# Define a view function to provide a book detail view
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
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
