from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index_Demo', views.index_Demo),
]
