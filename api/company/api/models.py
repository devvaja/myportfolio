from django.db import models

# Create your models here.
class Company(models.Model):
    cmp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    type = models.CharField(max_length=100,choices=(('IT','IT'),
                                                   ('NON IT','NON IT',),
                                                    ('MOBILE','MOBILE')
                                                    ))


class Employee(models.Model):
    name = models.CharField(max_length=50)
    work = models.CharField(max_length=50)
    salary = models.IntegerField()
