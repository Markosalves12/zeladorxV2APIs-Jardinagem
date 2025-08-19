from django.urls import path
from catalogo_de_servicos.api.view_jardinagem import (ListCatalogodeServicoJardinagem, CatalogoServicosJardinagemUpdate,
                                                      CatalogoServicosJardinagemDetail, CatalogoServicosJardinagemAlterStatus,
                                                      CreateCatalogoServicosJardinagem,
                                                      IfDeleteServicoCatalogoJardinagem,
                                                      ListCatalogodeServicoJardinagemFromForms,
                                                      DeleteServicoCatalogoJardinagem)


urlpatterns = [
    path('ListCatalogodeServicoJardinagem/', ListCatalogodeServicoJardinagem.as_view(), name="ListCatalogodeServicoJardinagem"),
    path('ListCatalogodeServicoJardinagemFromForms/', ListCatalogodeServicoJardinagemFromForms.as_view(), name="ListCatalogodeServicoJardinagemFromForms"),
    path('CatalogoServicosJardinagemUpdate/<str:id_random>/', CatalogoServicosJardinagemUpdate, name="CatalogoServicosJardinagemUpdate"),
    path('CatalogoServicosJardinagemDetail/<str:id_random>/', CatalogoServicosJardinagemDetail, name="CatalogoServicosJardinagemDetail"),
    path('CatalogoServicosJardinagemAlterStatus/<str:id_random>/', CatalogoServicosJardinagemAlterStatus, name="CatalogoServicosJardinagemAlterStatus"),
    path('CreateCatalogoServicosJardinagem/', CreateCatalogoServicosJardinagem, name="CreateCatalogoServicosJardinagem"),
    path('IfDeleteServicoCatalogoJardinagem/<str:id_random>/', IfDeleteServicoCatalogoJardinagem, name="IfDeleteServicoCatalogoJardinagem"),
    path('DeleteServicoCatalogoJardinagem/<str:id_random>/', DeleteServicoCatalogoJardinagem, name="DeleteServicoCatalogoJardinagem"),
]