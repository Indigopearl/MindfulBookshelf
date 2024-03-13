import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Category


class BookshelfViewsTestCase(TestCase):
    def setUp(self):
        # Create a test category
        self.category1 = Category.objects.create(
            name="Category 1", description="Description 1"
        )
        self.category2 = Category.objects.create(
            name="Category 2", description="Description 2"
        )

        # Create some test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Author 1",
            description="Description 1",
            publication_date="2024-05-05",
            category=self.category1,
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Author 2",
            description="Description 2",
            publication_date="2024-05-05",
            category=self.category2,
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookshelf/home.html")

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookshelf/book_list.html")

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookshelf/about.html")

