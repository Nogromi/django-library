from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Book(models.Model):
    # book_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    book_author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


def get_deadline():
    return datetime.today() + timedelta(days=30)

class Formular(models.Model): #бібліотечна облікова картка, що вкладається в книжку, з відомостями про цю книжку і відмітками про  читача.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_option= models.TextField(default='reading_room',max_length=15)
    state = models.NullBooleanField(default=None)
    # two_weeks=datetime.date(0,0, 14)
    order_date = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_deadline)
    # return_date= models.DateTimeField(default=datetime.now()+timedelta(days=30))
    def __str__(self):
        return str(self.user.username) + ' - ' + self.book.title


class Record(models.Model):
    username = models.ForeignKey(User)
    time = models.DateTimeField()