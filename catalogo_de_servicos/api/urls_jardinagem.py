from django.urls import path
from catalogo_de_servicos.api.view_jardinagem import (ListCatalogodeServicoJardinagem, CatalogoServicosJardinsUpdate,
                                                      CatalogoServicosJardinsDetail, CatalogoServicosJardinsAlterStatus)


urlpatterns = [
    path('ListCatalogodeServicoJardinagem/', ListCatalogodeServicoJardinagem.as_view(), name="ListCatalogodeServicoJardinagem"),
    path('CatalogoServicosJardinsDetail/<str:id_random>/', CatalogoServicosJardinsDetail, name="CatalogoServicosJardinsDetail"),
    path('CatalogoServicosJardinsUpdate/<str:id_random>/', CatalogoServicosJardinsUpdate, name="CatalogoServicosJardinsUpdate"),
    path(
        'CatalogoServicosJardinsAlterStatus/<str:id_random>/',
         CatalogoServicosJardinsAlterStatus,
         name="CatalogoServicosJardinsAlterStatus"
    ),
 ]