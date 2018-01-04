from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required(login_url='../')
def home_view(request):
	return render(request, 'home.html')


@login_required(login_url='../')
def driver_view(request):
	return render(request, 'driver.html')