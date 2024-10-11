from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        r = User.objects.create_user(username=username,email=email,password=password)
        r.save()
        return redirect('/login/')
    return render(request,'register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/index/')
        else:
            messages.info(request, 'invalid credencial')
    return render(request,'login.html')


@login_required
def index(request):
    return render(request,'index.html')



@login_required
def videocall(request):
    return render(request,'videocall.html')

def Logout(request):
    logout(request)
    return render(request,'index.html')

def join(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect('/videocall/?roomID=' + roomID)
    return render(request, 'join.html')
