from django.urls import path
from servicos.api.views_configuracoes_limpeza_predial import (ListServicoLimpezaPredialConfigurado,
                                                              ServicosConfiguradosLimpezaPredialDetail,
                                                              CreateServicosConfiguradosLimpezaPredial,
                                                              ServicosConfiguradosLimpezaPredialUpdate,
                                                              ServicosConfiguradosLimpezaPredialAlterStatus,
                                                              IfDeleteServicoLimpezaPredialConfigurado,
                                                              DeleteServicoLimpezaPredialConfigurado)

urlpatterns = [
    path('ListServicoLimpezaPredialConfigurado/', ListServicoLimpezaPredialConfigurado.as_view(),
         name="ListServicoLimpezaPredialConfigurado"),

    path('ServicosConfiguradosLimpezaPredialDetail/<str:id_random>/', ServicosConfiguradosLimpezaPredialDetail,
         name="ServicosConfiguradosLimpezaPredialDetail"),

    path('CreateServicosConfiguradosLimpezaPredial/', CreateServicosConfiguradosLimpezaPredial,
         name="CreateServicosConfiguradosLimpezaPredial"),

    path('ServicosConfiguradosLimpezaPredialUpdate/<str:id_random>/',
         ServicosConfiguradosLimpezaPredialUpdate,
         name="ServicosConfiguradosLimpezaPredialUpdate"),

    path('ServicosConfiguradosLimpezaPredialAlterStatus/<str:id_random>/', ServicosConfiguradosLimpezaPredialAlterStatus,
         name="ServicosConfiguradosLimpezaPredialAlterStatus"),

    path('IfDeleteServicoLimpezaPredialConfigurado/<str:id_random>/',
         IfDeleteServicoLimpezaPredialConfigurado,
         name="IfDeleteServicoLimpezaPredialConfigurado"),

    path('DeleteServicoLimpezaPredialConfigurado/<str:id_random>/',
         DeleteServicoLimpezaPredialConfigurado,
         name="DeleteServicoLimpezaPredialConfigurado"),
]