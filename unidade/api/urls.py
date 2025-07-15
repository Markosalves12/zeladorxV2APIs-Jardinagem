from django.urls import path
from unidade.api.views import ListUnidade, IfDeleteUnidade, UnidadeDetail, UnidadeUpdate, UnidadeAlterStatus


urlpatterns = [
    path('ListUnidade/', ListUnidade.as_view(), name="ListUnidade"),
    path('IfDeleteUnidade/<str:id_random>/', IfDeleteUnidade, name="IfDeleteUnidade"),
    path('UnidadeDetail/<str:id_random>/', UnidadeDetail, name="UnidadeDetail"),
    path('UnidadeUpdate/<str:id_random>/', UnidadeUpdate, name="UnidadeUpdate"),
    path('UnidadeAlterStatus/<str:id_random>/', UnidadeAlterStatus, name="UnidadeAlterStatus"),
]