import json

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.template.base import logger

from .models import *
from .serializers import WebSerializer


# Create your views here.
def index(request):
    return render(request,'index.html')


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

    if request.method== 'POST':
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')

        else:
            messages.info(request,'Invalid Username and Password')
            return redirect('/register/')


    return render(request,'login.html')


def Logout(request):
    logout(request)
    return redirect('/')

def shop(request):
    c = Watch.objects.all()
    return render(request,'shop.html',{'c': c})


# def cart(request,wid):
#     w = Watch.objects.get(id=wid)
#     user = request.user.id
#     if Cart.objects.filter(user=user, watch=w.id):
#         c=Cart.objects.get(user=user, watch=w.id)
#         c.save()
#         return redirect('/cart/')
#
#     else:
#         p = Cart.objects.create(user_id=user, total=w.price, watch_id=w.id)
#         return redirect('/cart/')
#
#     return render(request, 'cart.html')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Watch, Cart

# @login_required
def cart(request, wid):
    watch = Watch.objects.get(id=wid)
    user_id = request.user.id
    cart_item, created = Cart.objects.get_or_create(user_id=user_id, watch_id=watch.id)

    if created:
        # If the item was just created, set its total price
        cart_item.total = watch.price
        cart_item.save()

    # Redirect to the cart page
    return redirect('/cart/')



# @login_required
def viewcart(request):
    user_id = request.user.id
    cart_items = Cart.objects.filter(user_id=user_id).select_related('watch')

    if not cart_items.exists():
        # Show an error message and redirect if the cart is empty
        messages.error(request, "Your cart is empty. Please check products.")
        return redirect('/cart/')  # Redirect to a relevant page

    # Calculate the total price of items in the cart
    total = sum(item.total for item in cart_items)
    subtotal = total

    # Render the cart template with cart items and total price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total,'subtotal':subtotal})


def checkout(request):
    return render (request,'checkout.html')

def contact(request):
    return render(request,'contact.html')


def watch(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        p = Watch.objects.create(name=name,price=price,image=image)
        p.save()
        return redirect('/shop/')
    return render(request,'shop.html')


def checkout(request):
    user=request.user.id
    items = Cart.objects.filter(user=user)
    total = sum(item.total for item in items)
    subtotal=total
    if not items:
        messages.error(request, "Your cart is empty. Please add products to your cart before proceeding to checkout.")
        return redirect('/cart/')

    return render(request,'checkout.html',{'total':total,'subtotal':subtotal,'items':items})

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
        zipcode = request.POST['zipcode']
        o = Order(name=name,email=email,address=address,number=number,city=city,zipcode=zipcode,user=request.user)
        o.save()
        print(o.id)

        for f in cart:
            cart_item = OrderItem(
                user_id=user.id,
                product_id=f.watch.id,
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

#
# def payment_view(request,):
#     if request.method == 'POST':
#         amount_str = request.POST.get('amount')
#
#         if not amount_str or not amount_str.isdigit():
#             return HttpResponse('Invalid amount')
#
#         amount = int(amount_str) * 100  # Amount in paise
#         currency = 'INR'
#         payment_capture = '1'
#
#         response = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture=payment_capture))
#
#         order_id = response['id']
#         order_status = response['status']
#
#         if order_status == 'created':
#             context = {
#                 'order_id': order_id,
#                 'amount': amount,
#                 'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#                 'currency': currency,
#             }
#             return render(request, 'payment.html', context)
#
#     return render(request, 'payment.html')
# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         try:
#             payment_data = json.loads(request.body)
#             order_id = payment_data['razorpay_order_id']
#             payment_id = payment_data['razorpay_payment_id']
#             signature = payment_data['razorpay_signature']
#
#             params_dict = {
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#
#             # Verify the payment signature
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#
#             if result is None:
#                 # Payment is successful
#                 # Save payment details in the database and perform other necessary actions
#                 return HttpResponse('Payment Success')
#             else:
#                 return HttpResponse('Payment Verification Failed')
#         except:
#             return HttpResponse('Invalid Payment Details')
#
#     return HttpResponse('Invalid Request')
# # views.py

def verify_payment(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            return JsonResponse({"status": "Payment verified successfully!"})
        except:
            return JsonResponse({"status": "Payment verification failed!"})


# views.py
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse


def create_razorpay_order(request):
    if request.method == "POST":
        amount = 50000  # Amount in paisa (500.00 INR)

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Create an order
        payment = client.order.create({
            "amount": amount,  # amount in paisa (500 INR)
            "currency": "INR",
            "payment_capture": "1"
        })

        # Pass order information to template for checkout
        context = {
            "payment": payment,
            "api_key": settings.RAZORPAY_API_KEY
        }

        return render(request, "checkout.html", context)

    return render(request, "checkout.html")



class WebView(APIView):

    def get(self,request):
        res = Web.objects.all()
        serializer = WebSerializer(res,many=True)
        return Response({"status":"success","Web":serializer.data}, status=status.HTTP_200_OK)

    def post(self,request):
        serializer =WebSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request,id):
        result = get_object_or_404(Web, id=id)
        print(result,'hgdgbajdujsjbj')
        serializer = WebSerializer(result,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success","data":serializer.data})
        else:
            return Response({"status":"error","data":serializer.errors})