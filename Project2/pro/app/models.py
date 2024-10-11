from datetime import timezone,datetime
from django.utils import timezone


from django.contrib.auth.models import User
from django.db import models



class Info(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='product')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.CharField(max_length=50, default=1)
    total = models.IntegerField()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage, e.g., 10 for 10%")


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


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    about=models.TextField()
    type = models.CharField(max_length=100,choices=(('IT','IT'),
                                                    ('NON IT','NON IT'),
                                                    ('MOBILE ','MOBILE')))
    DATE = models.DateTimeField(auto_now_add=True)