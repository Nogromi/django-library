from django import forms

from .models import Book, Formular


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields=('title', 'quantity', 'description', 'book_author')



class FormularForm(forms.ModelForm):
    class Meta:
        model = Formular
        fields=('state',)