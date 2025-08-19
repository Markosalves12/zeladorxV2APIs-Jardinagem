from django.urls import path
from areas.api.views_limpeza_predial import (ListAreasLimpezaPredial, AreasLimpezaPredialDetail,
                                             AreasLimpezaPredialUpdate, AreaLimpezaPredialAlterStatus,
                                             AreasAssociadasLocalidadeLimpezaPredial, CreateAreaLimpezaPredial,
                                             IfDeleteAreasLimpezaPredial, ListAreasLimpezaPredialFromForms,
                                             DeleteAreasLimpezaPredial, TempoDesdeUltimoAtendimentoLimpezaPredial)


urlpatterns = [
    path('ListAreasLimpezaPredial/', ListAreasLimpezaPredial.as_view(), name="ListAreasLimpezaPredial"),
    path('AreasLimpezaPredialDetail/<str:id_random>/', AreasLimpezaPredialDetail, name="AreasLimpezaPredialDetail"),
    path('AreasLimpezaPredialUpdate/<str:id_random>/', AreasLimpezaPredialUpdate, name="AreasLimpezaPredialUpdate"),
    path('AreaLimpezaPredialAlterStatus/<str:id_random>/', AreaLimpezaPredialAlterStatus, name="AreaLimpezaPredialAlterStatus"),
    path('AreasAssociadasLocalidadeLimpezaPredial/<str:id_random>/', AreasAssociadasLocalidadeLimpezaPredial,
         name="AreasAssociadasLocalidadeLimpezaPredial"),
    path('CreateAreaLimpezaPredial/', CreateAreaLimpezaPredial, name="CreateAreaLimpezaPredial"),
    path('IfDeleteAreasLimpezaPredial/<str:id_random>/', IfDeleteAreasLimpezaPredial, name="IfDeleteAreasLimpezaPredial"),
    path('ListAreasLimpezaPredialFromForms/', ListAreasLimpezaPredialFromForms.as_view(), name="ListAreasLimpezaPredialFromForms"),
    path('DeleteAreasLimpezaPredial/<str:id_random>/', DeleteAreasLimpezaPredial, name="DeleteAreasLimpezaPredial"),
    path('TempoDesdeUltimoAtendimentoLimpezaPredial/', TempoDesdeUltimoAtendimentoLimpezaPredial, name="TempoDesdeUltimoAtendimentoLimpezaPredial"),
]