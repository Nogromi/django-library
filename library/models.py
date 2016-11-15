from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Book(models.Model):
    # book_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    description = models.TextField()
    book_author = models.CharField(max_length=100)



    def __str__(self):
        return self.title


class Formular(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

