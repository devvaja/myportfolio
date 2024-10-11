from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from login import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
import django.utils.encoding
from .tokens import generate_token
from django.utils.http import urlsafe_base64_decode


# Create your views here.
def home(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already taken')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,'email already exists')
            return redirect('home')

        if len(username)>10:
            messages.error(request,'username must be greater than 10')
            return redirect('home')

        if password != confirm_password:
            messages.error(request,'password not matched')
            return redirect('home')


        if not username.isalnum():
            messages.error(request,'userrname must be AlphaNumeric')
            return redirect('home')


        s=User.objects.create_user(username=username,email=email,
                                password=password,)
        s.first_name=firstname
        s.last_name=lastname
        s.is_active = False
        s.save()
        messages.success(request,"Account Created")

        # email
        subject = 'Welcome to email '
        message = "hello" + s.first_name + 'Welcome to our website /n' + 'We have sent a confirmation email to your account'
        for_email = settings.EMAIL_HOST_USER
        to_list = [s.email]
        send_mail(subject,message,for_email,to_list,fail_silently=True)

        # Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @Dev !!!"
        message2 = render_to_string('email.html',{
            'name': s.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(django.utils.encoding.force_bytes(s.pk)),
            'token': generate_token.make_token(s)
        })
        email = EmailMessage(
            email_subject,
            message2,settings.EMAIL_HOST_USER,
            [s.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')


    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
            # firstname=User.first_name
            # return render(request,'index.html',{'firstname':firstname})

        else:
            messages.error(request,'unsuccesfull')
            return redirect('home')

    return render(request,'signin.html')

def signout(request):
        logout(request)
        messages.success(request,'successfully logged out!!!')
        return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        s = User.objects.get(pk=uid)

    except(TypeError,ValueError,OverflowError,User.DoesNotExits):
        s=None

    if s is not None and generate_token.check_token(s,token):
        s.is_active = True
        s.save()
        login(request,s)
        return redirect('home')
    else:
        return render(request,'activation_fail.html')
