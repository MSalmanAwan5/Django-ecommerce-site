from django.shortcuts import render, redirect
from .models import Addresses
from .forms import AddressForm
from billing.models import BillingProfile
from django.utils.http import is_safe_url


def address_checkout_create_view(request):
    form = AddressForm(request.POST or None)
    print(request.POST)
    next_ = request.GET.get('next')
    next_post_ = request.POST.get('next')

    redirect_path = next_ or  next_post_ or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        address_type = request.POST.get('address_type','shipping')
        if billing_profile is not None:
            instance.address_type = address_type
            instance.billing_profile = billing_profile
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")

        else:
            return redirect("cart:checkout")
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        return redirect('checkout:home')


def address_checkout_reuse_view(request):
    if request.user.is_authenticated():
        print(request.POST)
        next_ = request.GET.get('next')
        next_post_ = request.POST.get('next')
        redirect_path = next_ or  next_post_ or None
        if request.method == "POST":
            shipping_address = request.POST.get('shipping_address', None)
            billing_profile, created = BillingProfile.objects.new_or_get(request)
            address_type = request.POST.get('address_type', 'shipping')
            # print("shipping address :" + shipping_address)
            qs = Addresses.objects.filter(billing_profile=billing_profile, id = shipping_address)
            if qs.exists():
                request.session[address_type + "_address_id"] = shipping_address
                # print(address_type + "_address_id")
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
            else:
                return redirect('checkout:home')
    return redirect('checkout:home')
