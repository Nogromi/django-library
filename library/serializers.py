from rest_framework import serializers
from .models import Book, Formular


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields= ('id', 'title', 'quantity', 'description', 'book_author')

class FormularSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formular
        fields=('id', 'user', 'book', 'user_option', 'state', 'order_date','deadline')


