"""ecommerece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from accounts.views import logout_view, index, login_page, register_page, guest_register_view
from .views import contact
from django.conf.urls import include
from django.views.generic import TemplateView
from cart.views import cart_home, cart_detail_api_view
from addresses.views import address_checkout_create_view, address_checkout_reuse_view

urlpatterns = [
    url(r'^register/', register_page,name='signup'),
    url(r'^login/', login_page, name='login'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # url(r'^settings/$',.settings, name='settings'),
    # url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^address/checkout/create/', address_checkout_create_view, name='address_checkout_create'),
    url(r'^address/checkout/reuse/', address_checkout_reuse_view, name='address_checkout_reuse'),
    url(r'^continue/guest', guest_register_view, name='guest_register'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^api/cart/', cart_detail_api_view, name='cart-api'),
    url(r'^cart/', include('cart.urls', namespace='carts')),
    url(r'^contact/', contact,name='contact'),
    url(r'^$', index, name="index"),
    url(r'^index/$', index),
    url(r'^admin/', admin.site.urls),
    url(r'products/',include('products.urls', namespace="products")),
    url(r'search/', include('search.urls', namespace="search")),
    url(r'bootstrap/',TemplateView.as_view(template_name="bootstrap/example.html")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'