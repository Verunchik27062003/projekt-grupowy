from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Review, User, Book, Author
from datetime import date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        labels = {
            'rating': 'Rating (1-5)',
            'content': 'Review',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }



class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email


class ComprehensiveReviewForm(forms.Form):
    # Fields for selecting existing book and author
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False, label="Existing Book")
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label="Existing Author")

    # Fields for new book and author (conditionally shown)
    new_book_title = forms.CharField(max_length=255, required=False, label="New Book Title")
    genre = forms.CharField(max_length=100, required=False, label="Genre")
    release_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    new_author_name = forms.CharField(max_length=255, required=False, label="New Author Name")
    nationality = forms.CharField(max_length=100, required=False, label="Author Nationality")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    # Review fields (always required)
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)
    content = forms.CharField(widget=forms.Textarea, label="Review Content", required=True)

    #Book cover image
    cover_image = forms.ImageField(required=False)

    def clean_release_date(self):
        release_date = self.cleaned_data.get('release_date')
        if release_date and release_date > date.today():
            raise ValidationError("Release date cannot be in the future.")
        return release_date

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError("Birth date cannot be in the future.")
        return birth_date

    def clean(self):
        cleaned_data = super().clean()

        # Check that at least one of the book or new_book_title is provided
        book = cleaned_data.get('book')
        new_book_title = cleaned_data.get('new_book_title')

        if not book and not new_book_title:
            raise forms.ValidationError("Please select an existing book or provide a new book title.")

        # Check that at least one of the author or new_author_name is provided
        author = cleaned_data.get('author')
        new_author_name = cleaned_data.get('new_author_name')

        if not author and not new_author_name:
            raise forms.ValidationError("Please select an existing author or provide a new author name.")

        return cleaned_data
