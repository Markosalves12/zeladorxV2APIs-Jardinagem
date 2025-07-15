from django.urls import path
from gerente.api.views_limpeza_predial import (ListGerenteLimpezaPredial, GerenteLimpezaPredialDetail,
                                               GerenteLimpezaPredialUpdate, GerenteLimpezaPredialAlterStatus)


urlpatterns = [
    path('ListGerenteLimpezaPredial/', ListGerenteLimpezaPredial.as_view(), name="ListGerenteLimpezaPredial"),
    path('GerenteLimpezaPredialDetail/<str:id_random>/', GerenteLimpezaPredialDetail, name="GerenteLimpezaPredialDetail"),
    path('GerenteLimpezaPredialUpdate/<str:id_random>/', GerenteLimpezaPredialUpdate, name="GerenteLimpezaPredialUpdate"),
    path('GerenteLimpezaPredialAlterStatus/<str:id_random>/', GerenteLimpezaPredialAlterStatus, name="GerenteLimpezaPredialAlterStatus"),
 ]