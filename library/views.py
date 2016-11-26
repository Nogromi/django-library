from  django.contrib.auth import *
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from  rest_framework import generics
import logging

from library import singleton
from library.forms import BookForm, FormularForm
from .models import Formular
from .serializers import *

logger = logging.getLogger(__name__)                                         # logger


def login_form(request):
    return render(request, 'library/login_form.html', {})


def home(request):                                                           # HOME
    books = Book.objects.order_by('title')
    formulars = Formular.objects.all()

    if request.method == "POST":
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                singleton.SystemLog(user)
                logger.warning('user \'' + user.username + '\'' + ' entered')

                if username == 'LibraryMan':
                    return render(request, 'library/libraryman_home.html', {'formulars': formulars, 'books': books})

                return render(request, 'library/home.html', {'books': books})
        else:
            logger.error('user \'' + str(user) + '\'' + ' tried to enter ')
            eror = "Unable to log in. Please check that you have entered your login and password correctly."
            return render(request, 'library/error_message.html', {'eror': eror})
    else:
        if request.user.username =="LibraryMan":
            return render(request, 'library/libraryman_home.html', {'formulars': formulars, 'books': books})

        return render(request, 'library/home.html', {'books': books})


def logout_view(request):
    logout(request)
    return render(request, 'library/login_form.html')
    # Redirect to a success page.


def sign_up_form(request):                                                  # sign up
    return render(request, 'library/sign_up_form.html', {})


def create_account(request):
    username = request.POST['u']
    password = request.POST['p']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    check_user = User.objects.filter(username=username)
    if len(check_user) > 0:
        eror = 'this login already taken'
        return render(request, 'library/error_message.html', {'eror': eror})
    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    user.save()
    books = Book.objects.order_by('title')
    return render(request, 'library/home.html', {'books': books})


def search_book(request):
    if request.method == "POST":
        book = request.POST['search_book']
        books = Book.objects.filter(title__contains=book)
        return render(request, 'library/book_list.html', {'books': books})
    else:
        books = Book.objects.all()
        return render(request, 'library/book_list.html', {'books': books})





def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    return render(request, 'library/book_detail.html', {'book': book})


def order_book(request, pk):                                                 # order book
    book = get_object_or_404(Book, pk=pk)
    user = request.user
    if book.quantity > 0:
        get_book = Book.objects.filter(title=book)[0]  # без [0]  це QuerySet а так це обэкт Книга

        if not Formular.objects.filter(user=user, book=get_book):
            # get_book= Book.objects.update(quantity=book.quantity-1)
            get_book.quantity -= 1
            get_book.save()
            option = request.POST['option']

            f = Formular(book=book, user=user, user_option=option)
            f.save()

            return render(request, 'library/order_book.html', {'book': book})
        else:
            eror = "You already have this book"
            return render(request, 'library/error_message.html', {'eror': eror})

    eror = "book have ended"
    return render(request, 'library/error_message.html', {'eror': eror})


def profile(request):
    # картка, що заповнюється на кожного читача бібліотеки, куди записуються відомості про видані йому книжки
    book_reader = Formular.objects.filter(user=request.user)
    return render(request, 'library/profile.html', {'book_reader': book_reader})


def return_book(request):
    book = request.POST['book_return']
    get_book = Book.objects.filter(title=book)[0]
    get_book.quantity += 1
    get_book.save()

    user = request.user
    f = Formular.objects.filter(user=user, book=get_book)
    f.delete()

    book_reader = Formular.objects.filter(user=request.user)

    return render(request, 'library/profile.html', {'book_reader': book_reader})


def add_book(request):
    return render(request, 'library/add_book.html')


def save_new_book(request):
    title = request.POST['title']
    author = request.POST['author']
    description = request.POST['description']
    quantity = request.POST['quantity']
    num_quantity = int(quantity)
    books = Book.objects.order_by('title')
    book_exist = False
    for book in books:
        if book.title == title:
            book_exist = True

    if not book_exist:
        new_book = Book.objects.create(title=title, book_author=author, description=description, quantity=quantity)
        new_book.save()
    else:
        eror = 'That book already exist. You can use edit button'
        return render(request, 'library/error_message.html', {'eror': eror})

    return render(request, 'library/libraryman_home.html', {'books': books})


def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect(book_detail, pk=book.pk)
            # return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_edit.html', {'form': form})

def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book.save()
            return redirect(book_detail, pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_edit.html', {'form': form})

def formular_list(request):
    formulars=Formular.objects.all()
    return render(request, 'library/formular_list.html', {'formulars':formulars})
def formular_detail(request, pk):
    formular = get_object_or_404(Formular, pk=pk)

    return render(request, 'library/formular_detail.html', {'formular': formular})

def formular_edit(request, pk):
    formular = get_object_or_404(Formular, pk=pk)
    if request.method == "POST":
        form = FormularForm(request.POST, instance=formular)
        if form.is_valid():
            formular.save()
            return redirect(book_detail, pk=formular.pk)
    else:
        form = FormularForm(instance=formular)
    return render(request, 'library/formular_edit.html', {'form': form})


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FormularList(generics.ListCreateAPIView):
    queryset = Formular.objects.all()
    serializer_class = FormularSerializer


class FormularDetail(generics.RetrieveUpdateDestroyAPIView
                     ):
    queryset = Formular.objects.all()
    serializer_class = FormularSerializer
