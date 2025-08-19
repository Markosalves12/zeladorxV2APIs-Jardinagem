from django.urls import path
from servicos.api.views_fato_servico_limpeza_predial import (CreateFatoServicoLimpezaPredial,
                                                             FatoServicoLimpezaPredialDetail,
                                                             FatoServicoLimpezaPredialUpdate,
                                                             ListFatoServicoLimpezaPredialByservico,
                                                            ListFatoServicoLimpezaPredial,
                                                             IfDeleteFatoServicoLimpezaPredial,
                                                             DeleteFatoServicoLimpezaPredial
                                                             )

urlpatterns = [
    path('ListFatoServicoLimpezaPredialByservico/<str:id_random>/', ListFatoServicoLimpezaPredialByservico,
         name="ListFatoServicoLimpezaPredialByservico"),

    path('FatoServicoLimpezaPredialDetail/<str:id_random>/', FatoServicoLimpezaPredialDetail,
         name="FatoServicoLimpezaPredialDetail"),

    path('CreateFatoServicoLimpezaPredial/<str:id_random>/', CreateFatoServicoLimpezaPredial,
         name="CreateFatoServicoLimpezaPredial"),

    path('FatoServicoLimpezaPredialUpdate/<str:id_random>/', FatoServicoLimpezaPredialUpdate,
         name="FatoServicoLimpezaPredialUpdate"),

    path('ListFatoServicoLimpezaPredial/', ListFatoServicoLimpezaPredial,
         name="ListFatoServicoLimpezaPredial"),

    path('IfDeleteFatoServicoLimpezaPredial/<str:id_random>/', IfDeleteFatoServicoLimpezaPredial,
         name="IfDeleteFatoServicoLimpezaPredial"),

    path('DeleteFatoServicoLimpezaPredial/<str:id_random>/', DeleteFatoServicoLimpezaPredial,
         name="DeleteFatoServicoLimpezaPredial"),
]