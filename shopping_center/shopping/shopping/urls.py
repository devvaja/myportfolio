"""
URL configuration for shopping project.

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
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('shop/', views.shop),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('cart/', views.viewcart, name='viewcart'),
    path('change_qty/<int:id>/', views.changeqty),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/', views.payment_view, name='payment'),
    path('checkout/', views.checkout),
    path('contact/', views.contact),
    path('login/', views.Login),
    path('placeorder/', views.placeorder),
    path('deleteCart/<int:id>/', views.deleteCart),

    path('logout/', views.Logout),
    path('product_details/<int:id>', views.product_details,name='product_details'),
    path('register/', views.register,name='Login'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)