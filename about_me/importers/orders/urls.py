from django.conf.urls import url
from about_me.importers.orders import views


urlpatterns = [
   url(r'^$', views.index, name='orders'),
   # url(r'^GETvalues/', views.GETvalues, name='GETvalues'),
   # url(r'^changeDB/', views.changeDB, name='changeDB'),
]
