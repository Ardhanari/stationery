from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=254, default='')
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    category = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=2, decimal_places=0)
    # date_added = 

    def __str__(self):
        return self.name
