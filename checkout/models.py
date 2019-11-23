from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
from django_countries.fields import CountryField

# import custom user model too, when it's ready

class Order(models.Model):
    user = models.CharField(max_length=50, blank=False, null=True)
    full_name = models.CharField(max_length=50, blank=False)
    company = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=False)
    country = CountryField()
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "({0}) {1} - {2}, {3}".format(self.id, self.date, self.full_name, self.country.name)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False)
    product = models.ForeignKey(Product, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0}x {1} @ {2}".format(self.quantity, self.product.name, self.product.price)