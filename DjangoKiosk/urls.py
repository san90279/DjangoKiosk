from django.contrib import admin
from django.conf.urls import url  
from polls.views import home, login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',home),
    url(r'^login/$',login),
]
