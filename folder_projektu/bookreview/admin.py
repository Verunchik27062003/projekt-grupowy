from django.contrib import admin
from .models import Book, Author, Review, User

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'content')

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Review, ReviewAdmin)