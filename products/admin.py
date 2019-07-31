from django.contrib import admin
from .models import Products


# Register your models here.

class ProductModel(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = Products


admin.site.register(Products, ProductModel)
