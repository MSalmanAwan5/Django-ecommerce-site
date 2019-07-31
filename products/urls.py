from django.conf.urls import url, include
from rest_framework import routers
from .views import ProductList,ProductDetailSlugView, product_list_view, DetailView, product_detail_view, product_detail_slug_view, ProductFeaturedDetailView, ProductFeaturedDetailSlugView, ProductFeaturedListView
from products import views
router = routers.DefaultRouter()
router.register(r'products',views.ProductsView,'products')
urlpatterns = [
    url(r'^list/',ProductList.as_view(), name='list'),
    #url(r'^list-fbv/', product_list_view),
    #url(r'^detail-class/(?P<pk>\d+)/$', DetailView.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', product_detail_view),
    url(r'^detail/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    #url(r'^featured_detail/(?P<pk>\d+)/$',ProductFeaturedDetailView),
    url(r'^featured-detail/(?P<slug>[\w-]+)/$',ProductFeaturedDetailSlugView.as_view(), name='featured-detail'),

    #url(r'^featured_list/$',ProductFeaturedListView),
    url(r'api/', include(router.urls))

]