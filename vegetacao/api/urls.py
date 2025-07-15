from django.urls import path
from vegetacao.api.views import ListCatalogoVegetacao


urlpatterns = [
    path('ListCatalogoVegetacao/', ListCatalogoVegetacao.as_view(), name="ListCatalogoVegetacao"),
 ]