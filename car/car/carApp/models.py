from django.db import models

# Create your models here.
class Register(models.Model):
     username = models.CharField(max_length=50)
     email = models.CharField(max_length=50)
     password = models.IntegerField()



class Car(models.Model):
     name = models.CharField(max_length=50)
     type = models.CharField(max_length=50)
     model = models.IntegerField()
     fuel = models.CharField(max_length=10)
     total_amount = models.IntegerField()
     image = models.ImageField()
     image2 = models.ImageField()
     image3 = models.ImageField()
     image4 = models.ImageField()

     def __str__(self):
          return self.name


class Car_Category(models.Model):
     car = models.ForeignKey(Car,on_delete=models.CASCADE)


class Students(models.Model):
     first_name = models.CharField(max_length=200)
     last_name = models.CharField(max_length=200)
     address = models.CharField(max_length=200)
     roll_number = models.IntegerField()
     mobile = models.CharField(max_length=10)

     def __str__(self):
          return self.first_name + " " + self.last_name