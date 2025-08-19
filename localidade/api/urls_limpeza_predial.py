from django.urls import path
from localidade.api.views_limpeza_predial import (ListLocalidadeLimpezaPredial, LocalidadeLimpezaPredialDetail,
                                                  LocalidadeLimpezaPredialUpdate, LocalidadeLimpezaPredialAlterStatus,
                                                  IfDeleteLocalidadeLimpezaPredial, CreateLocalidadeLimpezaPredial,
                                                  ListLocalidadeLimpezaPredialFromForms, DeleteLocalidadeLimpezaPredial)


urlpatterns = [
    path('ListLocalidadeLimpezaPredial/', ListLocalidadeLimpezaPredial.as_view(), name="ListLocalidadeLimpezaPredial"),
    path('LocalidadeLimpezaPredialDetail/<str:id_random>/', LocalidadeLimpezaPredialDetail, name="LocalidadeLimpezaPredialDetail"),
    path('LocalidadeLimpezaPredialUpdate/<str:id_random>/', LocalidadeLimpezaPredialUpdate, name="LocalidadeLimpezaPredialUpdate"),
    path('LocalidadeLimpezaPredialAlterStatus/<str:id_random>/', LocalidadeLimpezaPredialAlterStatus, name="LocalidadeLimpezaPredialAlterStatus"),
    path('CreateLocalidadeLimpezaPredial/', CreateLocalidadeLimpezaPredial, name="CreateLocalidadeLimpezaPredial"),
    path('IfDeleteLocalidadeLimpezaPredial/<str:id_random>/', IfDeleteLocalidadeLimpezaPredial, name="IfDeleteLocalidadeLimpezaPredial"),
    path('ListLocalidadeLimpezaPredialFromForms/', ListLocalidadeLimpezaPredialFromForms.as_view(), name="ListLocalidadeLimpezaPredialFromForms"),
    path('DeleteLocalidadeLimpezaPredial/<str:id_random>/', DeleteLocalidadeLimpezaPredial, name="DeleteLocalidadeLimpezaPredial"),
]