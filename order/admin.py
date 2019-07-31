from django.contrib import admin
from .models import Order
# Register your models here.


class OrderModel(admin.ModelAdmin):
    list_display = ['__str__' ,'id']

    class Meta:
        model = Order


admin.site.register(Order, OrderModel)