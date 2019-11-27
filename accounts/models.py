from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    full_name = models.CharField(max_length=50, blank=False)
    company = models.CharField(max_length=50, blank=True)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=True)
    country = CountryField()
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "{0}\n{1}\n{2}\n{3}\n{4}".format(self.full_name, self.street_address1, self.street_address2, self.town_or_city, self.country.name)
