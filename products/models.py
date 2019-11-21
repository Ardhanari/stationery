from django.db import models

class ProductCategory(models.Model):
    """Category of the product"""

    name = models.CharField(max_length=254, default='All')

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
    variant = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    # status
    # created_at
    discount = models.DecimalField(max_digits=2, decimal_places=0)
    category = models.ForeignKey(ProductCategory)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return self.name    
