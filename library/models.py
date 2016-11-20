from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Book(models.Model):
    # book_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    book_author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Formular(models.Model): #бібліотечна облікова картка, що вкладається в книжку, з відомостями про цю книжку і відмітками про  читача.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_option= models.TextField(default='reading_room',max_length=15)

    def __str__(self):
        return str(self.user) + ' - ' + self.book.title
