from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from polls.views import home, login
from Auth.views import V_Login, V_CheckAuth
from EmployeeCard.views import V_EmployeeCardIndex,V_GetEmployeeCardData,V_EmployeeCardEdit,V_EmployeeCardSave
from Term.views import V_TermIndex,V_GetTermData,V_TermEdit,V_TermNew
from Penalty.views import V_PenaltyIndex,V_GetPenaltyData,V_PenaltyEdit,V_PenaltyNew




Auth_urlpatterns = [
    url(r'^login/$', V_Login),
    url(r'^home/$', V_CheckAuth),
]

EmployeeCard_urlpatterns = [
    path('index/', V_EmployeeCardIndex),
    path('GetEmployeeCardData/', V_GetEmployeeCardData),
    path('Edit/<int:id>/', V_EmployeeCardEdit),
    path('Save/', V_EmployeeCardSave),
]

Term_urlpatterns = [
    path('index/', V_TermIndex,name='TermIndex'),
    path('GetTermData/', V_GetTermData),
    path('Edit/<int:id>/', V_TermEdit,name='TermEdit'),
    path('Edit/', V_TermNew,name='TermNew'),
]
Penalty_urlpatterns = [
    path('index/', V_PenaltyIndex,name='PenaltyIndex'),
    path('GetPenaltyData/', V_GetPenaltyData),
    path('Edit/<int:id>/', V_PenaltyEdit,name='PenaltyEdit'),
    path('Edit/', V_PenaltyNew,name='PenaltyNew'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$',home),
    url(r'^login/$',login),
    url(r'^polls/', include('polls.urls')),
    url(r'^Auth/', include(Auth_urlpatterns)),
    path('EmployeeCard/', include(EmployeeCard_urlpatterns)),
    path('Term/', include(Term_urlpatterns)),
    path('Penalty/', include(Penalty_urlpatterns)),
]
