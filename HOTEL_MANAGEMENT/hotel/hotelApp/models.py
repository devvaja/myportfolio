from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import timezone

# Create your models here.


class Hotel(models.Model):
    name= models.CharField(max_length=50)
    price= models.IntegerField()
    details = models.CharField(max_length=50,null=True)
    image= models.ImageField(null=True)
    image2= models.ImageField(null=True)
    image3= models.ImageField(null=True)


class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    customers = models.IntegerField()
    rooms = models.IntegerField(default=1)
    number = models.IntegerField(default= None)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now_add=True)


class mybooking(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.SET_NULL,null=True)
    book = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    days =models.IntegerField()
    total = models.IntegerField(null=True)

