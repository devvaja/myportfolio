import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Category, Product,Wishlist,Promotion

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import razorpay

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
# @csrf_exempt
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

def home(request):
    return HttpResponse("hello"
                        "<a href='/index/'>Go</a>")


def index(request,cid=None):
    c = Category.objects.all()
    cid = request.GET.get('category')
    print(cid)

    if cid:
        ciid = Category.objects.get(id=cid)
        print(ciid)
        p = Product.objects.filter(name=ciid)
        print(p)
    else:
        p = Product.objects.all()

    return render(request, 'index.html',{'c': c, 'p': p})


def shop(request,cid=None):
    cat = Category.objects.all()
    cid=request.GET.get('category')
    print(cid)

    if cid:
        ciid = Category.objects.get(id=cid)
        print(ciid)
        p=Product.objects.filter(name=ciid)
        print(p)
    else:
       p = Product.objects.all()

    # print(p)
    return render(request,'shop.html',{'cat':cat,'p':p})

# def viewProduct(request,id):
#     p= Product.objects.get(id=id)
#     p.product_name = product_name
#     p.product_description = product_description
#     p.product_price = product_price
#     p.product_image = product_image
#     p.save()
#
#     return render(request,'shop.html',{'p':p})

def cart(request,pid):
    user=request.user.id
    # print(user)
    proid=Product.objects.get(id=pid)
    # print(proid)
    if Cart.objects.filter(user=user,product=proid.id):
        c=Cart.objects.get(user=user,product=proid.id)
        print(c.quantity)
        c.quantity = int(c.quantity) + 1
        c.total=c.quantity * c.total
        c.save()
        print(c.quantity)
        return  redirect('/cart/')

    else:
        p = Cart.objects.create(user_id=user,total=proid.product_price, product_id=proid.id)
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


# @login_required
def add_to_wishlist(request, product_id):
    user = request.user

    product = Product.objects.get(id=product_id)
    if Wishlist.objects.filter(user=user,product=product):
        # print('already in whishlist')
        messages.info(request, 'Already Added To Wishlist')
    else:
        wishlist_item = Wishlist.objects.create(user=user,product=product)
        messages.success(request, 'Added to Wishlist')


        # return HttpResponse('product added in wishlist')
    return redirect('/wishlist/')


# @login_required
def wishlist(request):
    userid=request.user
    wishlist_items = Wishlist.objects.filter(user=userid)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def deleteProduct(request,wishlist_item_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Item removed from wishlist')
    return redirect('/wishlist/')
def changeqty(request,id):
    c=Cart.objects.get(id=id)
    print(c,'cccccccccccccc')
    new_quantity = request.POST['qty']
    print(new_quantity,'nq')
    if new_quantity == 0:
        c.delete()
        return redirect('/cart/')
    else:    # Get the updated quantity from the form
        c.quantity = new_quantity
        c.total = c.product.product_price * int(new_quantity)
        c.save()
        return redirect('/cart/')


def deleteCart(request,id):
    c = Cart.objects.get(id=id)
    c.delete()
    return redirect('/cart/')


def about(request):
    return render(request, template_name='about.html')


def bbq(request):
    return render(request, template_name='bbq pizza.html')


def contact(request):
    return render(request, template_name='contact.html')


def gallary(request):
    return render(request, template_name='gallary.html')


def menu1(request):
    return render(request, template_name='menu1.html')


def menu2(request):
    return render(request, template_name='menu2.html')


def menuispote2(request):
    return render(request, template_name='menuispote2.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

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

        r = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password=password)
        r.save()
        return redirect("/login/")
    return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print(user, 'user')
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credencial')
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('/')


def productDetails(request,id):
    product = Product.objects.get(id=id)

    return render(request,'productDetails.html',{'product':product})


def checkout(request):
    user = request.user.id
    cart_items = Cart.objects.filter(user=user)
    promotions = Promotion.objects.all()

    if not cart_items:
        messages.error(request, "Your cart is empty. Please add products to your cart before proceeding to checkout.")
        return redirect('/cart/')

    sub_total = sum(item.total for item in cart_items)
    discount = 0
    promotion_code = request.POST.get('promotion_code')

    if promotion_code:
        try:
            promotion = Promotion.objects.get(code=promotion_code)
            discount = (promotion.discount / 100) * sub_total
        except Promotion.DoesNotExist:
            messages.error(request, "Invalid promotion code.")

    shipping_charge = 25  # Adjust as needed
    estimated_tax = 20  # Adjust as needed
    total = sub_total - discount + shipping_charge + estimated_tax




    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'discount': discount,
        'shipping_charge': shipping_charge,
        'estimated_tax': estimated_tax,
        'total': total,
        'promotion_code': promotion_code,
        'promotion':promotions,
        # 'razorpay_client':razorpay_client,
        # 'client':client
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



from rest_framework import viewsets
from .models import *
from .serializers import *

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer







