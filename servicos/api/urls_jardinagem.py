from django.urls import path
from servicos.api.views_jardinagem import (# ListServicoJardinagemAgendado,
                                           # ListFatoServicoJardinagem,
                                           ListServicoJardinagemAgendadoAnotados,
                                           ListDetailFatoServicoJardinagem)


urlpatterns = [
    # path('ListServicoJardinagemAgendado/', ListServicoJardinagemAgendado.as_view(),
    #      name="ListServicoJardinagemAgendadoSerializer"),

    # path('ListFatoServicoJardinagem/', ListFatoServicoJardinagem.as_view(),
    #      name="ListFatoServicoJardinagemSerializer"),

    path('ListServicoJardinagemAgendadoAnotados/', ListServicoJardinagemAgendadoAnotados.as_view(),
         name="ListServicoJardinagemAgendadoAnotados"),

    path('ListDetailFatoServicoJardinagem/<str:id_random>/', ListDetailFatoServicoJardinagem,
         name="ListDetailFatoServicoJardinagem"),
]