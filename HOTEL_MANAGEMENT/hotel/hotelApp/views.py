from itertools import count

from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render
from django.contrib.messages.middleware import MessageMiddleware
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def service(request):
    return render(request,'service.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')



def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        r = User.objects.create_user(username=username,email=email,password=password)
        r.save()
        return redirect('/login/')
    return render(request,'registration.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credencial')
    return render(request, 'registration.html')

def Logout(request):
    logout(request)
    return redirect("/")


login_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='/login/')
def create_room(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        details = request.POST['details']
        image = request.FILES['image']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        r= Hotel.objects.create(name=name,price=price,details=details,image=image,image2=image2,image3=image3)
        r.save()
        return redirect('/rooms/')
    return render(request,'rooms.html')


# login_required(redirect_field_name=Login,login_url=None)
login_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='/login')
def rooms(request):
    r = Hotel.objects.all()
    return render(request,'rooms.html',{'r':r})


def details(request,id):
    r= Hotel.objects.get(id=id)
    return render(request,'details.html',{"r":r})


def view_room(request,id):
    user=request.user
    room = Hotel.objects.get(id=id)
    return render(request,'booking.html',{"room":room,"user":user})

def get_details(request):
    user = request.user.id
    hotel = Hotel.objects.filter(user=user)


@login_required
def book(request, id):
    room = get_object_or_404(Hotel, id=id)
    user = request.user

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        customers = request.POST['customers']
        rooms = request.POST['rooms']
        number = request.POST['number']

        # Create a new booking object
        booking = Book.objects.create(
            user=user,
            hotel=room,
            name=name,
            email=email,
            customers=customers,
            rooms=rooms,
            number=number,
            check_in=check_in,
            check_out=check_out
        )
        booking.save()

        return redirect('booking_details', booking_id=booking.id)  # Redirect to booking details page

    return render(request, 'booking.html', {'room': room, 'user': user})


def booking_details(request, booking_id):
    # Fetch the booking object using the provided booking_id
    booking = get_object_or_404(Book, id=booking_id)

    # Pass the booking details to the template
    return render(request, 'booking_confirmation.html', {'booking': booking})














