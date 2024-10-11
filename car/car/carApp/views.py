from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.migrations import serializer
from django.shortcuts import render, redirect
from rest_framework import serializers, response, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .serializers import StudentSerializer


# from .. import car


# Create your views here.
def index(request):
    return render(request,'index.html')

def car_list(request):
    return render(request,'car_list.html')


def listing_your(request):
    return render(request,'listing_your.html')

def contact_us(request):
    return render(request,'contact_us.html')

def about_us(request):
    return render(request,'about_us.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = request.user

        if User.objects.filter(username=username):
            messages.error(request, 'Username already taken')
            return redirect('/register/')

        if User.objects.filter(email=email):
            messages.error(request, 'email already exists')
            return redirect('/register/')

        if len(username) > 10:
            messages.error(request, 'username must be greater than 10')
            return redirect('/register/')

        if not username.isalnum():
            messages.error(request, 'userrname must be AlphaNumeric')
            return redirect('/register/')
        r = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        r.save()
        return redirect('/login/')
    return render(request,'login.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credencial')

    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def add_car(request):
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']
        model = request.POST['model']
        fuel = request.POST['fuel']
        image = request.FILES['image']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        image4 = request.FILES['image4']
        total_amount = request.POST['total_amount']

        c= Car.objects.create(name=name,type=type,model=model,fuel=fuel,total_amount=total_amount,image=image,image2=image2,image3=image3,image4=image4)
        c.save()

    return render(request,'car_details.html')

def car_list_read(request):
    cars = Car.objects.all()
    for i in cars:
        print(i)
    return render(request, 'car_list.html', {'cars': cars})


def car_details(request,id):
    car = Car.objects.get(id=id)

    return render(request,'car_details.html',{'car':car})



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send the email
            send_mail(
                subject=f'New Contact Form Submission from {full_name}',
                message=f'Name: {full_name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=email,  # This will show as the sender's email
                recipient_list=['devvaja56@gmail.com'],  # Replace with your email
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})


import mysql.connector
# mydb=mysql.connector.connect(host="localhost",user="root",password="root")
# mycursor = mydb.cursor()
#
# mycursor.execute("Create Database CAR")
# print("Database Created")

# mydb=mysql.connector.connect(host="localhost",user='root',password='root',database='CAR')
# mycursor=mydb.cursor()
# mycursor.execute("CREATE TABLE Cars (NAME VARCHAR(50), MODEL INT)")
# print("Table created")

# mydb=mysql.connector.connect(host="localhost",user='root',password='root',database='CAR')
# # database=('class9am')
# # mycursor = mydb.cursor()
# # sql = 'INSERT INTO CARS (NAME, MODEL) VALUES ("SKODA", 2019)'
# #
# # mycursor.execute(sql)
# # mydb.commit()
# # print(mycursor.rowcount,'record inserted')
#
# mycursor = mydb.cursor()
# sql = "INSERT INTO cars (name, model) VALUES (%s, %s)"
# val = [('BENTLY', 2017), ('RENAULT', 2018), ('MAHINDRA', 2019)]
#
# mycursor.executemany(sql, val)
# mydb.commit()

# import mysql.connector
#
# mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='car')
# mycursur=mydb.cursor()
# # mycursur.execute("insert into cars(name,model) values ('mahindra',2019)")
# # mydb.commit()
#
# sql = "insert into cars (name, model) values (%s, %s)"
# val=[
#     ('suzuki',2001),
#     ('KIA',2022),
#     ('Honda',2014)
# ]
# mycursur.executemany(sql,val)
# mydb.commit()


class StudentView(APIView):

    def get(self,request):
        result = Students.objects.all()
        serializers = StudentSerializer(result,many=True)
        return Response({'status':'success','students':serializers.data},status=200)

    def post(self,request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)