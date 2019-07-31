from django.contrib import admin
from .models import BillingProfile
# Register your models here.

class BillingProfileModel(admin.ModelAdmin):
    list_display = ['email','id','timestamp','user']

    class Meta:
        model = BillingProfile

admin.site.register(BillingProfile, BillingProfileModel)