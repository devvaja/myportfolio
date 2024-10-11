# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, ProductImage

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        product = Product.objects.create(name=name, description=description, price=price)

        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('/productlist/') # Replace with your success URL

    return render(request, 'product.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})