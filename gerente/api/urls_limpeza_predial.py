from django.urls import path
from gerente.api.views_limpeza_predial import (ListGerenteLimpezaPredial, GerenteLimpezaPredialDetail,
                                               GerenteLimpezaPredialUpdate, GerenteLimpezaPredialAlterStatus,
                                               CreateGerenteLimpezaPredial, IfDeleteGerenteLimpezaPredial,
                                               DeleteGerenteLimpezaPredial, ListGerenteLimpezaPredialFromForms)


urlpatterns = [
    path('CreateGerenteLimpezaPredial/', CreateGerenteLimpezaPredial, name="CreateGerenteLimpezaPredial"),
    path('ListGerenteLimpezaPredial/', ListGerenteLimpezaPredial.as_view(), name="ListGerenteLimpezaPredial"),
    path('GerenteLimpezaPredialDetail/<str:id_random>/', GerenteLimpezaPredialDetail, name="GerenteLimpezaPredialDetail"),
    path('GerenteLimpezaPredialUpdate/<str:id_random>/', GerenteLimpezaPredialUpdate, name="GerenteLimpezaPredialUpdate"),
    path('GerenteLimpezaPredialAlterStatus/<str:id_random>/', GerenteLimpezaPredialAlterStatus, name="GerenteLimpezaPredialAlterStatus"),
    path('IfDeleteGerenteLimpezaPredial/<str:id_random>/', IfDeleteGerenteLimpezaPredial, name="IfDeleteGerenteLimpezaPredial"),
    path('DeleteGerenteLimpezaPredial/<str:id_random>/', DeleteGerenteLimpezaPredial, name="DeleteGerenteLimpezaPredial"),
path('ListGerenteLimpezaPredialFromForms/', ListGerenteLimpezaPredialFromForms.as_view(), name="ListGerenteLimpezaPredialFromForms"),
 ]