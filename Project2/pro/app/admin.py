from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Promotion)