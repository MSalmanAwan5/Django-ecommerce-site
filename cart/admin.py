from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Cart
# Register your models here.


class CartModel(admin.ModelAdmin):
    list_display = ['__str__' ,'id']

    class Meta:
        model = Cart


admin.site.register(Cart, CartModel)