from django.contrib import admin
from .models import Cart, Customer, Product, OrderPlaced, Adrs

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_disp = ['id', 'user', 'name', 'addres', 'city', 'pincode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_disp = ['id', 'title', 'mrp', 'selling_price', 'desc', 'category', 'product_image', 'quantity']

@admin.register(Cart)
class ProductModelAdmin(admin.ModelAdmin):
     list_disp = ['user', 'product', 'quant']

admin.site.register(OrderPlaced)
admin.site.register(Adrs)