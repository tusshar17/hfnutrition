from django.contrib import admin
from store.models import *

# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Category_Name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['Brand_Name', 'Brand_Contact', 'Brand_Logo']


class FlavourAdmin(admin.ModelAdmin):
    list_display = ['value']


class QuantityAdmin(admin.ModelAdmin):
    list_display = ['value']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['prod_name', 'category', 'brand',
                    'flavour', 'qty', 'mrp', 'selling_price', 'stock']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'img', 'img_type']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'password']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'qty']


class Address_BookAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'pin', 'state', 'district', 'city']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time', 'address', 'order_total', 'order_status']


class Order_LineAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'product', 'price', 'qty']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Flavour, FlavourAdmin)
admin.site.register(Quantity, QuantityAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Address_Book, Address_BookAdmin)
# admin.site.register(Order_status, OrderStatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Order_Line, Order_LineAdmin)
