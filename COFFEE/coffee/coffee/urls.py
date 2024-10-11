"""
URL configuration for coffee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import static
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('contact/', views.contact),
    path('coffee/', views.coffee,name='coffee'),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('register/', views.register),
    path('product/', views.product),
    # path('product_details/<int:id>', views.product_details,name='product_details'),
    path('cart/<int:pid>', views.cart,name='cart'),
    path('delete_cart/<int:id>/', views.delete_cart,name='delete_cart'),
    path('cart/', views.viewcart, name='viewcart'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)