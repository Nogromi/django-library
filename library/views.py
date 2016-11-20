from django.shortcuts import render
from django.contrib.auth.models import User
from  django.contrib.auth import *
from .models import Book
from django.shortcuts import render, get_object_or_404
from  rest_framework import generics
from .serializers import BookSerializer
from .models import Formular


def login_form(request):
    return render(request, 'library/login_form.html', {})


def home(request):
    if request.method=="POST":
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                books = Book.objects.order_by('title')
                return render(request, 'library/home.html', {'books': books} )
        else:
            return render(request, 'library/fuck.html')
    else:
        books = Book.objects.order_by('title')
        return render(request, 'library/home.html', {'books': books})


def sign_up_form(request):
    return render(request, 'library/sign_up_form.html', {})


def create_account(request):
    username = request.POST['u']
    password = request.POST['p']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    check_user = User.objects.filter(username=username)
    if len(check_user) > 0:
        return render(request, 'library/sign_up_form.html')
    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    user.save()
    books = Book.objects.order_by('title')
    return render(request, 'library/home.html', {'books': books})


def search_book(request):
    book = request.POST['search_book']
    books = Book.objects.filter(title__contains=book)
    return render(request, 'library/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)

    return render(request, 'library/book_details.html', {'book': book})




def order_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user
    if book.quantity > 0:
        get_book = Book.objects.filter(title=book)[0] # без [0]  це QuerySet а так це обэкт Книга

        if not Formular.objects.filter(user=user, book= get_book):
            # get_book= Book.objects.update(quantity=book.quantity-1)
            get_book.quantity -= 1
            get_book.save()
            option = request.POST['option']

            f = Formular(book=book, user=user, user_option=option)
            f.save()

            return render(request, 'library/order_book.html', {'book': book})
    return render(request, 'library/fuck.html')


def profile(request):

    # картка, що заповнюється на кожного читача бібліотеки, куди записуються відомості про видані йому книжки
    book_reader=Formular.objects.filter(user=request.user)
    return render(request, 'library/profile.html',{'book_reader':book_reader} )



def return_book(request):
    book = request.POST['book_return']
    get_book = Book.objects.filter(title=book)[0]
    get_book.quantity += 1
    get_book.save()

    user= request.user
    f= Formular.objects.filter(user=user, book=get_book)
    f.delete()

    book_reader=Formular.objects.filter(user=request.user)

    return render(request, 'library/profile.html',{'book_reader':book_reader} )


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer