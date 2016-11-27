from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from library import views

from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$', views.login_form, name='login_form'),
    url(r'^sign_up$', views.sign_up_form, name='sign up form'),
    url(r'^home$', views.home, name='home'),
    url(r'^index/home$', views.home, name='home'),
    url(r'^home/$', views.create_account),
    url(r'^search', views.search_book, name='search book'),
    url(r'^book/(?P<pk>[0-9]+)/$', views.book_detail, name='book detail'),
    url(r'^book/(?P<pk>[0-9]+)/order_book$', views.order_book, name='order book'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^return_book$', views.return_book, name='return_book'),
    url(r'^index/$', views.logout_view, name='logout'),
    url(r'^book/new/$', views.book_new, name='book_new'),
    url(r'^book/edit/$', views.book_new, name='book_new'),
    url(r'^book/(?P<pk>[0-9]+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^books/$', views.search_book, name='book_list'),
    url(r'^formulars/$', views.formular_list, name='formular_list'),
    url(r'^formular/(?P<pk>[0-9]+)/$', views.formular_detail, name='formular detail'),
    url(r'^formular/(?P<pk>[0-9]+)/edit/$', views.formular_edit, name='formular_edit'),
)
apiurls=[
    url(r'^book/$', views.BookList.as_view()),
    url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),

    url(r'formular/$', views.FormularList.as_view()),
    url(r'formular/(?P<pk>[0-9]+)/$', views.FormularDetail.as_view())
]
apiurls=format_suffix_patterns(apiurls)
urlpatterns +=apiurls