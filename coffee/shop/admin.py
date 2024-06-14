from django.contrib import admin
from .models import Product, Storage, Order, OrderProduct, Category, SliderItem

# Register your models here.

admin.site.register(Storage)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Category)
admin.site.register(SliderItem)
