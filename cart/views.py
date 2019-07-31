from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart
from order.models import Order
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Addresses
from billing.models import BillingProfile
from products.models import Products
from accounts.forms import loginForm, GuestForm


def cart_detail_api_view(request):
    print("cart api view")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{"name":x.title,"price":x.price, "url":x.get_absolute_url(), "id":x.id} for x in cart_obj.products.all()]
    data = {"products":products, "total":cart_obj.total, "subtotal":cart_obj.subtotal}
    return JsonResponse(data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    request.session["cart_items"] = cart_obj.products.count()
    return render(request, "carts/home.html", {"cart":cart_obj})


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            print("Product is gone")
            return redirect("carts:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("hello gee")
            data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(data)
        return redirect("carts:home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count()==0:
        return redirect("carts:home")


    login_form = loginForm()
    guest_form = GuestForm()
    shipping_address = AddressForm()

    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_address_id = request.session.get('billing_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Addresses.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if billing_address_id:
            del request.session['billing_address_id']
            order_obj.billing_address = Addresses.objects.get(id=billing_address_id)
        if shipping_address_id:
            del request.session['shipping_address_id']
            order_obj.shipping_address = Addresses.objects.get(id=shipping_address_id)
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == "POST":
        order_done = order_obj.check_done()
        if order_done:
            request.session["cart_items"] = 0
            order_obj.mark_paid()
            del request.session["cart_id"]
            return redirect('carts:success')

    context = {
        "billing_profile":billing_profile,
        "object":order_obj,
        "login_form":login_form,
        "guest_form":guest_form,
        "shipping_address_form":shipping_address,
        "address_qs":address_qs
    }

    return render(request, "carts/checkout_home.html",context)



def checkout_done(request):
    return render(request, "carts/checkout-success.html")