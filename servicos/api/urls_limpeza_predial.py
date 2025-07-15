from django.urls import path
from servicos.api.views_limpeza_predial import (ListServicoLimpezaPredialAgendado, ListFatoLimpezaPredial,
                                           ListServicoLimpezaPredialConfigurado)


urlpatterns = [
    path('ListServicoLimpezaPredialAgendado/', ListServicoLimpezaPredialAgendado.as_view(),
         name="ListServicoLimpezaPredialAgendado"),

    path('ListFatoLimpezaPredial/', ListFatoLimpezaPredial.as_view(),
         name="ListFatoLimpezaPredial"),

    path('ListServicoLimpezaPredialConfigurado/', ListServicoLimpezaPredialConfigurado.as_view(),
         name="ListServicoJardinagemConfigurado"),
 ]