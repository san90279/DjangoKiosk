from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from polls.views import home, login
from Auth.views import V_Login, V_CheckAuth
from EmployeeCard.views import V_EmployeeCardIndex,V_GetEmployeeCardData,V_EmployeeCardEdit,V_EmployeeCardSave
from Term.views import V_TermIndex,V_GetTermData,V_TermEdit
from Penalty.views import V_PenaltyIndex,V_GetPenaltyData,V_PenaltyEdit,V_PenaltyNew
from FeeItem.views import V_FeeItemIndex,V_GetFeeItemData,V_FeeItemEdit,V_FeeItemNew
from Store.views import V_StationIndex,V_GetStationData,V_StationEdit,V_StationNew,V_StoreNew


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
    path('index/', V_TermIndex),
    path('GetTermData/', V_GetTermData),
    path('Edit/<int:id>', V_TermEdit),
    path('Edit/', V_TermEdit),
]

Penalty_urlpatterns = [
    path('index/', V_PenaltyIndex,name='PenaltyIndex'),
    path('GetPenaltyData/', V_GetPenaltyData),
    #path('PenaltySearch/', V_PenaltySearch,name='PenaltySearch'),
    path('Edit/<int:id>/', V_PenaltyEdit,name='PenaltyEdit'),
    path('Edit/', V_PenaltyNew,name='PenaltyNew'),
]

FeeItem_urlpatterns = [
    path('index/', V_FeeItemIndex,name='FeeItemIndex'),
    path('GetFeeItemData/', V_GetFeeItemData),
    #path('PenaltySearch/', V_PenaltySearch,name='PenaltySearch'),
    path('Edit/<int:id>/', V_FeeItemEdit,name='FeeItemEdit'),
    path('Edit/', V_FeeItemNew,name='FeeItemNew'),
]

Invoice_urlpatterns = [

]

Deal_urlpatterns = [

]

Store_urlpatterns = [
    path('index/', V_StationIndex,name='StationIndex'),
    path('GetStationData/', V_GetStationData),
    #path('PenaltySearch/', V_PenaltySearch,name='PenaltySearch'),
    path('StationEdit/<int:id>/', V_StationEdit,name='StationEdit'),
    path('StationEdit/', V_StationNew,name='StationNew'),
    path('StoreEdit/', V_StoreNew,name='StoreNew'),
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
    path('FeeItem/', include(FeeItem_urlpatterns)),
    path('Invoice/', include(Invoice_urlpatterns)),
    path('Deal/', include(Deal_urlpatterns)),
    path('Store/', include(Store_urlpatterns)),
]
