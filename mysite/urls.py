from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from library import views

from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$', views.login_form, name='login_form'),
    # url(r'^', views.login_form, name='login_form'),
    url(r'^sign_up$', views.sign_up_form, name='sign up form'),
    url(r'^home$', views.home, name='home'),
    # url(r'^home/$', views.logged_home, name='logged home'),
    url(r'^home/$', views.create_account),
    url(r'^search', views.search_book, name='search book'),
    url(r'^book_details/(?P<pk>[0-9]+)/$', views.book_details, name='book details'),
    url(r'^book_details/(?P<pk>[0-9]+)/order_book$', views.order_book, name='order book'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^return_book$', views.return_book, name='return_book'),

    # url(r'^profile$', views.logged_profile, name='logged profile'),
    # url(r'^book/new/$', views.book_new, name='book_new'),
)
apiurls=[
    url(r'^book/$', views.BookList.as_view()),
    url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),

]
apiurls=format_suffix_patterns(apiurls)
urlpatterns +=apiurls