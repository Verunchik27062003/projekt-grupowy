from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    recommended = models.BooleanField(default=False)

    def average_rating(self):
        reviews = self.reviews.all()  # Assuming `related_name="reviews"` in Review
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return None  # No reviews yet

    def __str__(self):
        return self.title

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username


from django.conf import settings
from .models import Book
from datetime import datetime


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.name}'
