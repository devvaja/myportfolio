from .models import *
from rest_framework import serializers

class CompanySerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializes(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = '__all__'
        fields = ['name','salary']
        # exclude = ['id',]

