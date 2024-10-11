from django.shortcuts import render

# Create your views here.
from  rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import CompanySerializers,EmployeeSerializes

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializers

@api_view(['GET'])
def home(request):
    emp = Employee.objects.all()
    serializer = EmployeeSerializes(emp,many=True)
    return Response({'Status': 300,'payload': serializer.data}  )

@api_view(['POST'])
def emp_data(request):
    data = request.data
    serializer = EmployeeSerializes(data=request.data)
    if not serializer.is_valid():
        return Response({'Status': 403, 'message': 'Something Went Wrong'})

    serializer.save()

    return Response({'Status': 300,'payload':serializer.data,'message':'Success'}  )

