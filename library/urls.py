from django.conf.urls import url
from . import views
from  rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.login_form, name='login_form'),
    url(r'^sign_up$' , views.sign_up_form, name='sign up form'),
    url(r'^check$', views.check, name='check'),
    url(r'^create_account', views.create_account, name='create account'),
    url(r'^search', views.search_book, name='search book'),
    url(r'^book_details/(?P<pk>[0-9]+)/$', views.book_details, name='book details'),
    url(r'^book_details/(?P<pk>[0-9]+)/order_book/$', views.order_book, name='order book'),


]

apiurls=[
    url(r'^book/$', views.BookList.as_view()),
    url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),

]
apiurls=format_suffix_patterns(apiurls)
urlpatterns +=apiurls