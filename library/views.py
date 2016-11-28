from  django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from  rest_framework import generics
import logging

from library import singleton
from library.forms import BookForm, FormularForm
from .models import Formular
from .serializers import *

logger = logging.getLogger(__name__)  # logger


def index(request):
    return render(request, 'library/login_form.html', {})


def login_form(request):
    return render(request, 'library/login_form.html', {})


def home(request):  # HOME
    books = Book.objects.order_by('title')

    if request.method == "POST":
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                singleton.SystemLog(user)
                logger.warning('user \'' + user.username + '\'' + ' entered')

                if request.user.groups.all()[0].name == "library_man":
                    formulars = Formular.objects.filter(state=None)

                    new_formulars = formulars.count()
                    return render(request, 'library/libraryman_home.html',
                                  {'formulars': formulars, 'books': books, 'new_formulars': new_formulars})

                return render(request, 'library/home.html', {'books': books})
        else:
            logger.error('user \'' + str(user) + '\'' + ' tried to enter ')
            eror = "Unable to log in. Please check that you have entered your login and password correctly."
            return render(request, 'library/error_message.html', {'eror': eror})
    else:

        if request.user.groups.all()[0].name == "library_man":
            formulars = Formular.objects.filter(state=None)

            new_formulars = formulars.count()
            return render(request, 'library/libraryman_home.html',
                          {'formulars': formulars, 'books': books, 'new_formulars': new_formulars})

        return render(request, 'library/home.html', {'books': books})


def logout_view(request):
    logout(request)
    return render(request, 'library/login_form.html')
    # Redirect to a success page.


def sign_up_form(request):  # sign up
    return render(request, 'library/sign_up_form.html', {})


def create_account(request):
    username = request.POST['u']
    password = request.POST['p']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    check_user = User.objects.filter(username=username)
    if len(check_user) > 0:
        eror = 'sorry, this login already taken'
        return render(request, 'library/error_message.html', {'eror': eror})
    g = Group.objects.filter(name='user')

    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    user.groups.add(g[0])

    user.save()
    # books = Book.objects.order_by('title')
    return redirect(login_form)


def search_book(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            book = request.POST['search_book']
            books = Book.objects.filter(title__contains=book)
            if request.user.groups.all()[0].name == "library_man":
                formulars = Formular.objects.filter(state=None)

                new_formulars = formulars.count()

                return render(request, 'library/libraryman_book_list.html',
                              {'books': books, 'new_formulars': new_formulars})

            return render(request, 'library/book_list.html', {'books': books})
        else:
            books = Book.objects.all()

            if request.user.groups.all()[0].name == "library_man":
                formulars = Formular.objects.filter(state=None)

                new_formulars = formulars.count()
                return render(request, 'library/libraryman_book_list.html',
                              {'books': books, 'new_formulars': new_formulars})
            else:
                return render(request, 'library/book_list.html', {'books': books})
    else:
        return redirect(index)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.user.groups == 'library_man':
        return render(request, 'library/libraryman_book_detail.html', {'book': book})

    return render(request, 'library/book_detail.html', {'book': book})


def order_book(request, pk):  # order book
    if request.user.is_authenticated():
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
    else:
        return redirect(index)


@login_required(login_url='/index')
def profile(request):
    # картка, що заповнюється на кожного читача бібліотеки, куди записуються відомості про видані йому книжки
    my_orders = Formular.objects.filter(user=request.user)
    return render(request, 'library/profile.html', {'my_orders': my_orders})


@login_required(login_url='/index')
def return_book(request):
    book = request.POST['book_return']
    get_book = Book.objects.filter(title=book)[0]
    get_book.quantity += 1
    get_book.save()

    user = request.user
    f = Formular.objects.filter(user=user, book=get_book)
    f.delete()

    my_orders = Formular.objects.filter(user=request.user)

    return render(request, 'library/profile.html', {'my_orders': my_orders})


@login_required(login_url='/index')
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


@login_required(login_url='/index')
def book_edit(request, pk):
    if request.user.groups == 'library_man':

        book = get_object_or_404(Book, pk=pk)
        if request.method == "POST":
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                book.save()
                return redirect(book_detail, pk=book.pk)
        else:
            form = BookForm(instance=book)
        return render(request, 'library/book_edit.html', {'form': form})
    else:
        return redirect(profile)


@login_required(login_url='/index')
def formular_list(request):
    formulars = Formular.objects.order_by('state')
    if request.user.groups.all()[0].name == "library_man":
        n = formulars.count()
        return render(request, 'library/libraryman_formular_list.html', {'formulars': formulars, 'n': n})
    else:
        return redirect(profile)


@login_required(login_url='/index')
def formular_detail(request, pk):
    if request.user.groups == 'library_man':

        formular = get_object_or_404(Formular, pk=pk)

        return render(request, 'library/formular_detail.html', {'formular': formular})
    else:
        return redirect(profile)


@login_required(login_url='/index')
def formular_edit(request, pk):
    if request.user.groups == 'library_man':

        formular = get_object_or_404(Formular, pk=pk)
        if request.method == "POST":
            form = FormularForm(request.POST, instance=formular)
            if form.is_valid():
                formular.save()
                return redirect(formular_list)
        else:
            form = FormularForm(instance=formular)
        return render(request, 'library/formular_edit.html', {'form': form})
    else:
        return redirect(profile)


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
