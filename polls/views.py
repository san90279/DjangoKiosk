from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
		return  render(request, 'index.html')

def login(request):
		return  render(request, 'login.html')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index_Demo(request):
	return  render(request, 'index-Demo.html')
