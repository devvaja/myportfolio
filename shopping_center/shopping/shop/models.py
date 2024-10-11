from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name=models.CharField(max_length=50)

    # Create your models here.
class Product(models.Model):
    cat= models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)
    price=models.IntegerField(null=True)
    image=models.ImageField()

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    address=models.CharField(max_length=254)
    number=models.IntegerField()
    country = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    city = models.CharField(max_length=50)

    class Meta:
        db_table='order'
        verbose_name_plural='Order'

    def __str__(self):
        return f"{self.user.username}-{self.id}"

class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    datetime=models.DateTimeField(default=timezone.now)

    class Meta:
        db_table='Order_item'
        verbose_name_plural='Order Items'


    def __str__(self):
        return f"OrderItem: {self.product.name} for {self.user.username}"
