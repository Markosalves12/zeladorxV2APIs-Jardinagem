from django.urls import path
from servicos.api.views_configuracoes_jardinagem import (ListServicoJardinagemConfigurado,
                                                         ServicosConfiguradosJardinsDetail,
                                                         CreateServicosConfiguradosJardins,
                                                         ServicosConfiguradosJardinagemUpdate,
                                                         ServicosConfiguradosJardinsAlterStatus,
                                                         DeleteServicoJardinagemConfigurado,
                                                         IfDeleteServicoJardinagemConfigurado)

urlpatterns = [
    path('ListServicoJardinagemConfigurado/', ListServicoJardinagemConfigurado.as_view(),
         name="ListServicoJardinagemConfigurado"),

    path('ServicosConfiguradosJardinsDetail/<str:id_random>/', ServicosConfiguradosJardinsDetail,
         name="ServicosConfiguradosJardinsDetail"),

    path('CreateServicosConfiguradosJardins/', CreateServicosConfiguradosJardins,
         name="CreateServicosConfiguradosJardins"),

    path('ServicosConfiguradosJardinagemUpdate/<str:id_random>/', ServicosConfiguradosJardinagemUpdate,
         name="ServicosConfiguradosJardinagemUpdate"),

    path('ServicosConfiguradosJardinsAlterStatus/<str:id_random>/', ServicosConfiguradosJardinsAlterStatus,
         name="ServicosConfiguradosJardinsAlterStatus"),

    path('IfDeleteServicoJardinagemConfigurado/<str:id_random>/', IfDeleteServicoJardinagemConfigurado,
         name="IfDeleteServicoJardinagemConfigurado"),

    path('DeleteServicoJardinagemConfigurado/<str:id_random>/', DeleteServicoJardinagemConfigurado,
         name="DeleteServicoJardinagemConfigurado"),
]