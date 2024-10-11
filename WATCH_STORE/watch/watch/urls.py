"""
URL configuration for watch project.

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
from django.contrib import admin
from django.urls import path
from watchApp import views
from django.conf import settings
from django.conf.urls.static import static

# from watch.watchApp.views import WebView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('shop/',views.shop),
    path('login/', views.Login),
    path('logout/', views.Logout,name='Logout'),
    path('register/', views.register),
    path('cart/<int:wid>/', views.cart,name='cart'),
    # path('change_qty/<int:id>/', views.changeqty),
    path('cart/', views.viewcart,),
    path('checkout/', views.checkout),
    path('contact/', views.contact),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    # path('payment/', views.payment_view, name='payment'),
    path('placeorder/', views.placeorder),
    path('checkout/', views.create_razorpay_order, name='checkout'),
    # path('payment/success/', views.payment_success, name='payment_success'),
    path('',views.WebView.as_view()),
    path('Web/<int:id>/', views.WebView.as_view(), name='patch'),
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)