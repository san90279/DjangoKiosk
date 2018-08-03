from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.http import HttpResponseRedirect


# Create your views here.
def V_Login(request):
	auth.logout(request)
	return  render(request, 'login.html')


def V_CheckAuth(request):
	username = request.POST.get('inputEmail', '')
	password = request.POST.get('inputPassword', '')
	user = auth.authenticate(username=username, password=password)


	if user is not None and user.is_active:
		auth.login(request, user)
		if user.is_superuser:
			return HttpResponseRedirect('/admin/')
		else:
			return  render(request, 'index.html')
	else:
		return  render(request, 'index.html')
