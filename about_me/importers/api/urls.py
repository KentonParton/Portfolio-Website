from django.conf.urls import url
from about_me.importers.api import views


urlpatterns = [
    # url(r'^orders/$', views.OrderListView.as_view(), name='order.list'),
    url(r'^vV8KkUmBsaZ8W5S9M6HD/$', views.OrderListView.as_view(), name='order.list'),
    
    url(r'^3RCNP7qYXcmG8jTsHSTm/$', views.ProductItemListView.as_view(), name='product.list'),
    # url(r'^products/$', views.ProductItemListView.as_view(), name='product.list'),
]