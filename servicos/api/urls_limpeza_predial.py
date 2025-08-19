from django.urls import path
from servicos.api.views_limpeza_predial import (CreateServicosLimpezaPredial, ServicosLimpezaPredialDetail,
                                                ServicosLimpezaPredailUpdate, IfDeleteServicoAgendadoLimpezaPredial,
                                                ListServicoLimpezaPredialAgendadoAnotados,
                                                alterar_status_servico_limpeza_predial, DeleteServicoAgendadoLimpezaPredial)


urlpatterns = [
    path('ListServicoLimpezaPredialAgendadoAnotados/', ListServicoLimpezaPredialAgendadoAnotados.as_view(),
         name="ListServicoLimpezaPredialAgendadoAnotados"),

    path('CreateServicosLimpezaPredial/', CreateServicosLimpezaPredial,
         name="CreateServicosLimpezaPredial"),

    path('ServicosLimpezaPredialDetail/<str:id_random>/', ServicosLimpezaPredialDetail,
         name="ServicosLimpezaPredialDetail"),

    path('ServicosLimpezaPredailUpdate/<str:id_random>/', ServicosLimpezaPredailUpdate,
         name="ServicosLimpezaPredailUpdate"),

    path('IfDeleteServicoAgendadoLimpezaPredial/<str:id_random>/', IfDeleteServicoAgendadoLimpezaPredial,
         name="IfDeleteServicoAgendadoLimpezaPredial"),

    path('AlterStatusServicoLimpezaPredial/<str:id_random>/', alterar_status_servico_limpeza_predial,
         name="AlterStatusServicoLimpezaPredial"),

    path('DeleteServicoAgendadoLimpezaPredial/<str:id_random>/', DeleteServicoAgendadoLimpezaPredial,
         name="DeleteServicoAgendadoLimpezaPredial"),
 ]