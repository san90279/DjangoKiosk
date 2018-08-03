from django.contrib import admin
from django.conf.urls import url,include
from polls.views import home, login
from Auth.views import V_Login, V_CheckAuth


Auth_urlpatterns = [
    url(r'^login/$', V_Login),
    url(r'^home/$', V_CheckAuth),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',home),
    url(r'^login/$',login),
    url(r'^polls/', include('polls.urls')),
    url(r'^Auth/', include(Auth_urlpatterns)),
]
