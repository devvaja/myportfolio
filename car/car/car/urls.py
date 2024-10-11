"""
URL configuration for car project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path
from carApp import views
from django.conf import settings
from django.conf.urls.static import static

# from car.carApp.views import StudentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('car_list/', views.car_list_read),
    path('listing_your/', views.listing_your),
    path('contact_us/', views.contact_us),
    path('about_us/', views.about_us),
    path('register/', views.register),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('car_details/<int:id>', views.car_details),
    # path('cars/', views.car_list_read, name='car_list'),
    path('', views.StudentView.as_view())

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)