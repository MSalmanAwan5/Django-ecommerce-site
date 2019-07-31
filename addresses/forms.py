from django import forms
from .models import Addresses

class AddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = [
        #'billing_profile',
        #'address_type',
        'address_line1',
        'address_line2',
        'province',
        'city' ,
        'country',
        'postal_code']