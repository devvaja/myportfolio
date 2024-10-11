from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return HttpResponse("Welcome"
                        '<a href="/index/">HTML</a>')
def index(request):
    return render(request, template_name='inndex.html')

def create(request):
    if request.method == 'POST':
        organization=request.POST['organization']
        leader=request.POST['leader']
        advisor=request.POST['advisor']
        destination=request.POST['destination']
        date=request.POST['date']
        email=request.POST['email']
        contact=request.POST['contact']
        city=request.POST['city']
        t=Travel.objects.create(organization=organization,leader=leader,advisor=advisor,
                                destination=destination,date=date,email=email,
                                contact=contact,city=city)
        return HttpResponse('data created')
    return render(request,'create.html')

def read(request):
    t=Travel.objects.all()
    return render(request,'read.html',{'t':t})