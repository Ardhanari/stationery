from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class ProductCategory(models.Model):
    """Category of the product"""

    name = models.CharField(max_length=254)

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    """Single product"""
    name = models.CharField(max_length=254, default='', blank=False)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    variant = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    # status
    created_at = models.DateField()
    discount = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    category = models.ForeignKey(ProductCategory)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return self.name    

class ProductReview(models.Model):
    """Defines reviews given by users to products they purchased"""
    title = models.CharField(max_length=254, default='', blank=False)
    review_text = models.TextField(blank=False)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    author = models.ForeignKey(User)