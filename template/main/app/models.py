from django.db import models

# Create your models here.
class Travel(models.Model):
    organization= models.CharField(max_length=50)
    leader= models.CharField(max_length=50)
    advisor= models.CharField(max_length=50)
    destination= models.CharField(max_length=50)
    date= models.DateField()
    email= models.CharField(max_length=50)
    contact= models.IntegerField()
    city= models.CharField(max_length=50)

