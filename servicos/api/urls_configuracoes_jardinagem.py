from django.urls import path
from servicos.api.views_configuracoes_jardinagem import ListServicoJardinagemConfigurado, ServicosConfiguradosJardinsDetail

urlpatterns = [
    path('ListServicoJardinagemConfigurado/', ListServicoJardinagemConfigurado.as_view(),
         name="ListServicoJardinagemConfigurado"),
    path('ServicosConfiguradosJardinsDetail/<str:id_random>/', ServicosConfiguradosJardinsDetail,
         name="ServicosConfiguradosJardinsDetail"),
]