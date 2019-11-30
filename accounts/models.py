from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class ShippingAddress(models.Model):
    user = models.OneToOneField(User)
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
        return "{0} ({1})\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}".format(self.full_name, self.company, self.street_address1, self.street_address2, 
                                                                    self.postcode, self.town_or_city, self.county, self.country.name)
