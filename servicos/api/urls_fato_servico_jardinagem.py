from django.urls import path
from servicos.api.views_fato_servico_jardinagem import (CreateFatoServicoJardinagem, FatoServicoJardinagemDetail,
                                                        FatoServicoJardinagemUpdate, ListFatoServicoJardinagemByservico,
                                                        ListFatoServicoJardinagem, IfDeleteFatoServicoJardinagem,
                                                        DeleteFatoServicoJardinagem
                                                        )

urlpatterns = [
    path('ListFatoServicoJardinagemByservico/<str:id_random>/', ListFatoServicoJardinagemByservico,
         name="ListFatoServicoJardinagemByservico"),

    path('ListFatoServicoJardinagem/', ListFatoServicoJardinagem,
         name="ListFatoServicoJardinagem"),

    path('FatoServicoJardinagemDetail/<str:id_random>/', FatoServicoJardinagemDetail,
         name="FatoServicoJardinagemDetail"),

    path('CreateFatoServicoJardinagem/<str:id_random>/', CreateFatoServicoJardinagem,
         name="CreateFatoServicoJardinagem"),

    path('FatoServicoJardinagemUpdate/<str:id_random>/', FatoServicoJardinagemUpdate,
         name="FatoServicoJardinagemUpdate"),

    path('IfDeleteFatoServicoJardinagem/<str:id_random>/', IfDeleteFatoServicoJardinagem,
         name="IfDeleteFatoServicoJardinagem"),

    path('DeleteFatoServicoJardinagem/<str:id_random>/', DeleteFatoServicoJardinagem,
         name="DeleteFatoServicoJardinagem"),
]

