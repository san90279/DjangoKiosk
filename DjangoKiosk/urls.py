from django.contrib import admin
from django.conf.urls import url,include
from polls.views import home, login
from Auth.views import V_Login, V_CheckAuth
from EmployeeCard.views import V_EmployeeCardIndex

Auth_urlpatterns = [
    url(r'^login/$', V_Login),
    url(r'^home/$', V_CheckAuth),
]

EmployeeCard_urlpatterns = [
    url(r'^index/$', V_EmployeeCardIndex),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',home),
    url(r'^login/$',login),
    url(r'^polls/', include('polls.urls')),
    url(r'^Auth/', include(Auth_urlpatterns)),
    url(r'^EmployeeCard/', include(EmployeeCard_urlpatterns)),
]
