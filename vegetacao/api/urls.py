from django.urls import path
from vegetacao.api.views import (ListCatalogoVegetacao, CreateVegetacao, VegetacaoUpdate, VegetacaoDetail,
                                 VegetacaoAlterStatus, ListCatalogoVegetacaoFromForms,
                                 IfDeleteCatalogoVegetacao, DeleteCatalogoVegetacao)


urlpatterns = [
    path('ListCatalogoVegetacao/', ListCatalogoVegetacao.as_view(), name="ListCatalogoVegetacao"),
    path('CreateVegetacao/', CreateVegetacao, name="CreateVegetacao"),
    path('VegetacaoUpdate/<str:id_random>/', VegetacaoUpdate, name="VegetacaoUpdate"),
    path('VegetacaoDetail/<str:id_random>/', VegetacaoDetail, name="VegetacaoDetail"),
    path('VegetacaoAlterStatus/<str:id_random>/', VegetacaoAlterStatus, name="VegetacaoAlterStatus"),
    path('ListCatalogoVegetacaoFromForms/', ListCatalogoVegetacaoFromForms.as_view(), name="ListCatalogoVegetacaoFromForms"),
    path('IfDeleteCatalogoVegetacao/<str:id_random>/', IfDeleteCatalogoVegetacao, name="IfDeleteCatalogoVegetacao"),
    path('DeleteCatalogoVegetacao/<str:id_random>/', DeleteCatalogoVegetacao, name="DeleteCatalogoVegetacao"),
]