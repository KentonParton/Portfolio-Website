from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from about_me.importers.core.views import home_view, logout_view, driver_view
from about_me.importers.orders import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', home_view, name='home'),
    url(r'^driver/$', driver_view, name='driver'),
    url(r'^logout/$', logout_view, name="logout"),
	url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),

    url(r'^orders/', include('about_me.importers.orders.urls')),
    url(r'^api/', include('about_me.importers.api.urls')),

    url(r'^GETvalues/', views.GETvalues, name='GETvalues'),
	url(r'^changeDB/', views.changeDB, name='changeDB'),
]
