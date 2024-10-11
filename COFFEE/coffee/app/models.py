from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.IntegerField()

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    total=models.IntegerField()
    quantity = models.CharField(max_length=50, default=1)
