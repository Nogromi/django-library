import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from library.models import Book, Formular


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title='TBook1', quantity=10, description="good gescription", book_author="Author A. A.")

    def test_book_contains(self):
        books = Book.objects.all()
        b = books[0]
        self.assertEqual(b.title, "TBook1")

    def test_change_book(self):
        books = Book.objects.all()
        b = books[0]
        b.title = "TBook2"
        self.assertEqual(b.title, "TBook2")


class FormularTestCase(TestCase):
    def setUp(self):
        b = Book.objects.create(title='ТКнига1', quantity=10, description="хороший опис книги",
                                book_author="Кльовий А. В.")
        u = User.objects.create(username='Юзер', first_name='ім\'я', last_name='прізвище')
        Formular.objects.create(user=u, book=b, user_option='reading_room', state=True,
                                order_date=datetime.date.today(),
                                deadline=datetime.date.today() + datetime.timedelta(days=30))

    def test_formular_contains(self):
        formulars = Formular.objects.all()
        f = formulars[0]
        self.assertEqual(f.__str__(), "Юзер - ТКнига1")
        self.assertEqual(f.book.title, "ТКнига1")
        self.assertEqual(f.user.username, "Юзер")

    def test_change_state(self):
        formulars = Formular.objects.all()
        f = formulars[0]
        f.state = False
        self.assertEqual(f.state, False)
