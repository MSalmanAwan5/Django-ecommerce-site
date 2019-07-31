from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from products.models import Products
# Create your views here.

class SearchProductView(ListView):
    template_name = "search/results.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        query=self.request.GET.get('q')
        context['query'] = query
        return context
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        print(query)
        request = self.request
        if query is not None:
            #print(Products.objects.search(query))
            return Products.objects.search(query)
        else:
            return Products.objects.filter(title__iexact='5656648811')