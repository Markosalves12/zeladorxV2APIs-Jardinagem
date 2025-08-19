from django.urls import path
from servicos.api.views_jardinagem import (ListServicoJardinagemAgendadoAnotados,
                                           CreateServicosJardinagem, ServicosJardinagemDetail,
                                           ServicosJardinagemUpdate, IfDeleteServicoAgendadoJardinagem,
                                           alterar_status_servico_jardinagem, DeleteServicoAgendadoJardinagem)


urlpatterns = [
    path('CreateServicosJardinagem/', CreateServicosJardinagem,
         name="CreateServicosJardinagem"),

    path('ServicosJardinagemDetail/<str:id_random>/', ServicosJardinagemDetail,
         name="ServicosJardinagemDetail"),

    path('ServicosJardinagemUpdate/<str:id_random>/', ServicosJardinagemUpdate,
         name="ServicosJardinagemUpdate"),

    path('ListServicoJardinagemAgendadoAnotados/', ListServicoJardinagemAgendadoAnotados.as_view(),
         name="ListServicoJardinagemAgendadoAnotados"),

    path('IfDeleteServicoAgendadoJardinagem/<str:id_random>/', IfDeleteServicoAgendadoJardinagem,
         name="IfDeleteServicoAgendadoJardinagem"),

    path('AlterStatusServicoJardinagem/<str:id_random>/', alterar_status_servico_jardinagem,
         name="AlterStatusServicoJardinagem"),

    path('DeleteServicoAgendadoJardinagem/<str:id_random>/', DeleteServicoAgendadoJardinagem,
         name="DeleteServicoAgendadoJardinagem"),
]