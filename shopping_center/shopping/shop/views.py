import json

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')



def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')


def register(request):
    if request.method =="POST":
        username=request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        r=User.objects.create_user(username=username,email=email,password=password)
        r.save()
        return redirect('/login/')
    return render(request,'login.html')
def Login(request):

    if request.method =="POST":
        username=request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        print(user,'hfwsfjlkdhhhhhhhhhhhhhhhhh')
        if user is not None:
            login(request,user)
            print(user,'hiiiiiiiiiiiiiiiii')

            return redirect('/')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('/login/')
            print('error')

    return render(request,'login.html')

def Logout(request):
    logout(request,)
    return redirect("/")

def create_product(request):
    if request.method == 'post':
        name=request.post['name']
        price=request.post['price']
        image=request.FILES['image']
        c=Product.objects.create(name=name,price=price,image=image)
        c.save()
    return render(request,'shop.html')


def product_details(request,id):
    p=Product.objects.get(id=id)
    return render(request,'product_details.html',{'p':p})


def shop(request,cid=None):
    c = Category.objects.all()
    cid = request.GET.get('category')
    if cid:
        ciid=Category.objects.get(id=cid)
        p=Product.objects.filter(name=ciid)
    else:
        p=Product.objects.all()
    return render(request,'shop.html',{'c':c,'p':p})

def cart(request,id):
    user=request.user.id
    pid = Product.objects.get(id=id)
    if Cart.objects.filter(user=user,product=pid):
        c=Cart.objects.get(user=user,product=pid)
        print(c.quantity)
        c.quantity = int(c.quantity) + 1
        c.total = c.quantity * c.total
        c.save()
        print(c.quantity)
        return redirect('/cart/')

    else:
        p = Cart.objects.create(user_id=user,total=pid.price, product_id=pid.id)
        return redirect('/cart/')


def viewcart(request):
    user = request.user.id
    c = Cart.objects.filter(user=user)
    product_count = c.count()

    # Check if the cart is empty first
    if not c.exists():
        messages.error(request, "Your cart is empty, please check product.")
        return render(request, 'cart.html', {'c': c, 'total': 0, 'product_count': 0})

    # Calculate the total considering the quantity of each item
    total = sum(item.product.price * item.quantity for item in c)

    return render(request, 'cart.html', {'c': c, 'total': total, 'product_count': product_count})


def deleteCart(request,id):
    c = Cart.objects.get(id=id)
    c.delete()
    return redirect('/cart/')


def changeqty(request, id):
    # Retrieve the cart item by its ID
    c = Cart.objects.get(id=id)

    # Get the updated quantity from the form, convert to integer
    new_quantity = int(request.POST.get('qty', 1))

    # Check if the new quantity is less than or equal to zero
    if new_quantity <= 0:
        c.delete()
        messages.success(request, "Item removed from the cart.")
        return redirect('/cart/')

    # Update the cart item with the new quantity
    c.quantity = new_quantity
    c.total = c.product.price * new_quantity
    c.save()

    messages.success(request, "Quantity updated successfully.")
    return redirect('/cart/')


def checkout(request):
    user = request.user.id
    cart_items = Cart.objects.filter(user=user)

    print(cart_items)
    if not cart_items:
        messages.error(request, "Your cart is empty. Please add products to your cart before proceeding to checkout.")
        return redirect('/cart/')
    total = sum(item.total for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'checkout.html', context)


def placeorder(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    if request.method == 'POST':
        # user = request.user.id
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        number = request.POST['number']
        city = request.POST['city']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        o = Order(name=name,email=email,address=address,number=number,city=city,country=country,zipcode=zipcode,user=request.user)
        o.save()
        print(o.id)

        for f in cart:
            cart_item = OrderItem(
                user_id=user.id,
                product_id=f.product.id,
                order_id=o.id,
            )
            cart_item.save()
            print(cart_item, 'oooooooooooooooooooooooooooooiiitemmmmmmmmmmmmm')

            cart_item.delete()
            print('deleted')


            client = razorpay.Client(auth=('rzp_test_ytoQRUzHn3jtXL', 'Sc3eDMyJEuNfGzcf5r5eWiLz'))
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        return redirect('/')

    else:
        HttpResponse('done')


print("RAZORPAY_KEY_ID:", settings.RAZORPAY_KEY_ID)
print("RAZORPAY_KEY_SECRET:", settings.RAZORPAY_KEY_SECRET)


def payment_view(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')

        if not amount_str or not amount_str.isdigit():
            return HttpResponse('Invalid amount')

        amount = int(amount_str) * 100  # Amount in paise
        currency = 'INR'
        payment_capture = '1'

        response = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture=payment_capture))

        order_id = response['id']
        order_status = response['status']

        if order_status == 'created':
            context = {
                'order_id': order_id,
                'amount': amount,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'currency': currency,
            }
            return render(request, 'payment.html', context)

    return render(request, 'payment.html')
@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            payment_data = json.loads(request.body)
            order_id = payment_data['razorpay_order_id']
            payment_id = payment_data['razorpay_payment_id']
            signature = payment_data['razorpay_signature']

            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is None:
                # Payment is successful
                # Save payment details in the database and perform other necessary actions
                return HttpResponse('Payment Success')
            else:
                return HttpResponse('Payment Verification Failed')
        except:
            return HttpResponse('Invalid Payment Details')

    return HttpResponse('Invalid Request')

