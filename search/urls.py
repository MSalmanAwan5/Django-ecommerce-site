from django.conf.urls import url
from .views import SearchProductView
urlpatterns = [
    url(r'^list/', SearchProductView.as_view(), name='query'),
]