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
from django.conf.urls import url
from django.contrib import admin
from accounts.views import index, logout, login, signup, user_profile
from products.views import all_products, add_to_cart
from django.views import static
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"), # swap this later on with index.html from static pages app - 'welcome page' / alternatively make it display all_products as well
    url(r'^accounts/logout/$', logout, name="logout"),
    url(r'^accounts/signup/$', signup, name="signup"),
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/profile/$', user_profile, name="userprofile"),
    url(r'^products/allproducts/$', all_products, name="allproducts"),
    url(r'^products/addtocart/$', add_to_cart, name="addtocart"),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': MEDIA_ROOT})
]
