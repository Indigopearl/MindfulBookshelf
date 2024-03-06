from django.contrib import admin
from .models import Book, Category, ReadingStatus, ReadingHistory

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(ReadingStatus)
admin.site.register(ReadingHistory)
