from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class ShippingAddress(models.Model):
    user = models.ForeignKey(User)
    full_name = models.CharField(max_length=50, blank=False)
    company = models.CharField(max_length=50, blank=True)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    country = CountryField()
    phone_number = models.CharField(max_length=20, blank=False)
