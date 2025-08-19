from django.urls import path
from terrenos.api.views import (CreateTerreno, TerrenoUpdate, TerrenoAlterStatus, TerrenoDetail, ListTerrenos,
                                IfDeleteTerreno, ListTerrenosFromForms, DeleteTerreno)


urlpatterns = [
    path('ListTerrenos/', ListTerrenos.as_view(), name="ListTerrenos"),
    path('TerrenoDetail/<str:id_random>/', TerrenoDetail, name="TerrenoDetail"),
    path('TerrenoUpdate/<str:id_random>/', TerrenoUpdate, name="TerrenoUpdate"),
    path('TerrenoAlterStatus/<str:id_random>/', TerrenoAlterStatus, name="TerrenoAlterStatus"),
    path('CreateTerreno/', CreateTerreno, name="CreateTerreno"),
    path('IfDeleteTerreno/<str:id_random>/', IfDeleteTerreno, name="IfDeleteTerreno"),
    path('ListTerrenosFromForms/', ListTerrenosFromForms.as_view(), name="ListTerrenosFromForms"),
    path('DeleteTerreno/<str:id_random>/', DeleteTerreno, name="DeleteTerreno"),
]