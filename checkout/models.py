from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import ShippingAddress
from django.utils import timezone
from django_countries.fields import CountryField

class Order(models.Model):
    user = models.ForeignKey(User)
    address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT, blank=False)
    # just in case - plenty foreign keys
    # full_name = models.ForeignKey(ShippingAddress, blank=False)
    # company = models.ForeignKey(ShippingAddress, blank=True)
    # street_address1 = models.ForeignKey(ShippingAddress, blank=False)
    # street_address2 = models.ForeignKey(ShippingAddress, blank=True)
    # postcode = models.ForeignKey(ShippingAddress, blank=True)
    # town_or_city = models.ForeignKey(ShippingAddress, blank=False)
    # county = models.CharField(max_length=40, blank=True)
    # country = CountryField()
    # below original model built at the beginning
    # full_name = models.CharField(max_length=50, blank=False)
    # company = models.CharField(max_length=50, blank=True)
    # phone_number = models.CharField(max_length=20, blank=False)
    # country = CountryField()
    # postcode = models.CharField(max_length=20, blank=True)
    # town_or_city = models.CharField(max_length=40, blank=False)
    # street_address1 = models.CharField(max_length=40, blank=False)
    # street_address2 = models.CharField(max_length=40, blank=False)
    # county = models.CharField(max_length=40, blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "({0}) {1} - {2}, {3}".format(self.id, self.date, self.address.full_name, self.address.country.name)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False)
    product = models.ForeignKey(Product, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0}x {1} @ {2}".format(self.quantity, self.product.name, self.product.price)