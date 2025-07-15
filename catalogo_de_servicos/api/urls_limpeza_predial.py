from django.urls import path
from catalogo_de_servicos.api.views_limpeza_predial import (ListCatalogodeServicoLimpezaPredial,
                                                            CatalogoServicosLimpezaPredialDetail,
                                                            CatalogoServicosLimpezaPredialUpdate, CatalogoServicosLimpezaPredialAlterStatus)


urlpatterns = [
    path('ListCatalogodeServicoLimpezaPredial/', ListCatalogodeServicoLimpezaPredial.as_view(), name="ListCatalogodeServicoLimpezaPredial"),
    path('CatalogoServicosLimpezaPredialDetail/<str:id_random>/', CatalogoServicosLimpezaPredialDetail, name="CatalogoServicosLimpezaPredialDetail"),
    path('CatalogoServicosLimpezaPredialUpdate/<str:id_random>/', CatalogoServicosLimpezaPredialUpdate, name="CatalogoServicosLimpezaPredialUpdate"),
    path('CatalogoServicosLimpezaPredialAlterStatus/<str:id_random>/', CatalogoServicosLimpezaPredialAlterStatus, name="CatalogoServicosLimpezaPredialAlterStatus"),
 ]