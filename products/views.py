from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from django.db.models import Q
from .models import Products
from django.views.generic import ListView, DetailView
from cart.models import Cart
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from rest_framework.views import APIView
import json
from corsheaders.signals import check_request_enabled
from django.core.paginator import Paginator

# Create your views here.


def ProductFeaturedListView(request):
    queryset = Products.objects.get_queryset().filter(featured=True)
    print(queryset)
    context = {
        "object_list": queryset,
    }
    return render(request, "product_list.html", context)


def ProductFeaturedDetailView(request, pk = None, *args, **kwargs):
    queryset = Products.objects.filter(Q(featured=True) & Q(pk=pk))
    print(queryset)
    context = {
        "object": queryset,
    }
    if queryset:
        return render(request, "featured_detail.html", context)
    else: raise Http404("Featured product with this id does not exist!")

    # return render(request, "product_featured_detail.html", context)


class ProductFeaturedDetailSlugView(DetailView):
    queryset = Products.objects.filter(Q(featured=True))
    template_name = "featured_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFeaturedDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            raise Http404("not found")
        except Products.MultiObjectsReturned:
            qs = Products.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Uhmm...")
        return instance

class ProductList(ListView):
    #queryset = Products.objects.all()
    template_name = "product_list.html"
    def get_queryset(self):
        request = self.request
        queryset = Products.objects.all()
        return queryset
    def get_context_data(self, *args, **kwargs):
        context = super(ProductList,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context




def product_list_view(request):
    queryset = Products.objects.all()
    print(queryset)
    context={
        "object_list":queryset,
    }
    return render(request,"product_list.html",context)


class ProductDetail(DetailView):
    queryset = Products.objects.all()
    template_name = "product_detail.html"


def product_detail_view(request,pk = None, *args, **kwargs):

    queryset = get_object_or_404(Products, pk=pk)
    context={
        "object_list":queryset,
    }
    return render(request,"product_detail.html",context)

def product_detail_slug_view(request, slug = None, *args, **kwargs):

    queryset = get_object_or_404(Products, slug=slug)
    context={
        "object_list":queryset,
    }
    return render(request,"product_detail.html",context)



class ProductDetailSlugView(DetailView):
    queryset = Products.objects.all()
    template_name = "product_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self,*args ,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            raise Http404("not found")
        except Products.MultiObjectsReturned:
            qs = Products.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Uhmm...")
        return instance




class ProductsView(viewsets.ReadOnlyModelViewSet):       # add this
      serializer_class = ProductSerializer          # add this
      queryset = Products.objects.all()
      pagination_class = PageNumberPagination
      pagination_class.page_size = 5
      

