from django.urls import path
from areas.api.views_limpeza_predial import (ListAreasLimpezaPredial, AreasLimpezaPredialDetail,
                                             AreasLimpezaPredialUpdate, AreaLimpezaPredialAlterStatus,
                                             AreasAssociadasLocalidadeLimpezaPredial, CreateAreaLimpezaPredial)


urlpatterns = [
    path('ListAreasLimpezaPredial/', ListAreasLimpezaPredial.as_view(), name="ListAreasLimpezaPredial"),
    path('AreasLimpezaPredialDetail/<str:id_random>/', AreasLimpezaPredialDetail, name="AreasLimpezaPredialDetail"),
    path('AreasLimpezaPredialUpdate/<str:id_random>/', AreasLimpezaPredialUpdate, name="AreasLimpezaPredialUpdate"),
    path('AreaLimpezaPredialAlterStatus/<str:id_random>/', AreaLimpezaPredialAlterStatus, name="AreaLimpezaPredialAlterStatus"),
    path('AreasAssociadasLocalidadeLimpezaPredial/<str:id_random>/', AreasAssociadasLocalidadeLimpezaPredial,
         name="AreasAssociadasLocalidadeLimpezaPredial"),
    path('CreateAreaLimpezaPredial/', CreateAreaLimpezaPredial, name="CreateAreaLimpezaPredial"),
]