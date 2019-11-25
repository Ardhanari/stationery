"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import index, logout, login, signup, user_profile, view_order
from accounts import urls_reset
from products.views import all_products, single_product
from search.views import search_for_product
from shoppingcart.views import view_cart, add_to_cart, edit_cart
from checkout.views import checkout
from django.views import static
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', all_products, name="index"),
    url(r'^accounts/logout/$', logout, name="logout"),
    url(r'^accounts/signup/$', signup, name="signup"),
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/profile/$', user_profile, name="userprofile"),
    url(r'^accounts/vieworder/(?P<id>\d+)$', view_order, name="vieworder"),
    url(r'^password-reset/', include(urls_reset)),
    url(r'^products/all/$', all_products, name="allproducts"),
    url(r'^products/product/(?P<id>\d+)$', single_product, name="singleproduct"),
    url(r'^products/searchresult/$', search_for_product, name="searchresult"),
    url(r'^shoppingcart/addtocart/(?P<id>\d+)$', add_to_cart, name="addtocart"),
    url(r'^shoppingcart/viewcart/$', view_cart, name="viewcart"),
    url(r'^shoppingcart/editcart/(?P<id>\d+)$', edit_cart, name="editcart"),
    url(r'^checkout/$', checkout, name="checkout"),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': MEDIA_ROOT}),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]
