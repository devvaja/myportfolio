from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def coffee(request):
    i = Product.objects.all()
    cat = Category.objects.all()
    cid = request.GET.get('category')
    print(cid)

    if cid:
        ciid = Category.objects.get(id=cid)
        print(ciid)
        p = Product.objects.filter(name=ciid)
        print(p)
    else:
        p = Product.objects.all()
    # Fetch all products without any filters
    return render(request, 'coffee.html', {'i': i,'cat':cat})


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
        r = User.objects.create_user(username=username, email=email, password=password)
        r.save()
        return redirect('/login/')
    return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print(request.POST.get('username'))
        # print(request.POST.get('password'))

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credencial')
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('/')



def product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Save the product to the database
        p = Product.objects.create(name=name, price=price, description=description, image=image)
        p.save()

    return render(request,'coffee.html')

# def product_details(request,id):
#     p= Product.objects.get(id=id)
#     return render(request,'product_details.html',{'p':p})


def cart(request,pid):
    p=Product.objects.get(id=pid)
    user=request.user.id
    if Cart.objects.filter(user=user,product=p.id):
        c= Cart.objects.get(user=user,product=p.id)
        print(c.quantity)
        c.quantity = int(c.quantity) + 1
        c.total = c.quantity * c.total
        c.save()
        print(c.quantity)
        return redirect('/cart/')

    else:
        p = Cart.objects.create(user_id=user,total=p.price, product_id=p.id)
        return redirect('/cart/')


    return render(request,'cart.html')


def viewcart(request):
    user = request.user.id
    c = Cart.objects.filter(user=user)
    product_count = c.count()
    total=0

    # print(c)
    if not c:
        messages.error(request,"Your cart is empty please check product")

    else:

        total = sum(i.total for i in c)
        return render(request, 'cart.html', {'c': c, 'total': total, 'product_count': product_count})


    return render(request,'cart.html',{'c':c,'total':total})


def delete_cart(request,id):
    c = Cart.objects.get(id=id)
    c.delete()
    return redirect('/cart/')