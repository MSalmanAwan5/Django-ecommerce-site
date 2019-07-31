from django.contrib import admin
from .models import Addresses
# Register your models here.

class AddressesModel(admin.ModelAdmin):
    list_display = ['id','billing_profile','address_line1','address_type']
    class Meta:
        Meta = Addresses


admin.site.register(Addresses, AddressesModel)
