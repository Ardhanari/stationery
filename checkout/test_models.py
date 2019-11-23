from django.test import TestCase
from .models import Order
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class testOrderModel(TestCase):
    def test_fullname_cant_be_blank(self): 
        order = Order(full_name="")
        full_name = order.full_name
        self.assertRaises(ValidationError, full_name="")

    # def test_phonenumber_cant_be_all_zeros(self): 
    #     order = Order(full_name="Create a test", phone_number="0000000")
    #     # phone_number = order.phone_number
    #     self.assertRaises(ValidationError, phone_number="0000000")

    def test_company_is_blank(self):
        order = Order(full_name="name", company="")
        company_blank = order.company
        self.assertTrue(company_blank=="")
        
    # should fail but passes
    # def test_company_can_be_blank_without_an_error_raised(self):
    #     self.assertRaises(ValidationError, company="") 

    # def test_timezone_now(self):
    #     date = timezone.now()

    def test_date_returns_valid_date(self):
        order = Order(full_name="Joe Doe", postcode="01018", date=timezone.now())
        self.assertTrue(isinstance(order.date, datetime.date))