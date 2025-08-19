from django.urls import path
from areas.api.views_jardinagem import (ListAreasJardinagem, AreasJardinagemDetail, AreasJardinagemUpdate,
                                        AreasJardinagemAlterStatus, AreasAssociadasLocalidadeJardinagem,
                                        CreateAreaJardinagem,
                                        IfDeleteAreasJardinagem, ListAreasJardinagemFromFoms,
                                        TempoDesdeUltimoAtendimentoJardinagem, DeleteAreasJardinagem)


urlpatterns = [
    path('ListAreasJardinagem/', ListAreasJardinagem.as_view(), name="ListAreasJardinagem"),
    path('AreasJardinagemDetail/<str:id_random>/', AreasJardinagemDetail, name="AreasJardinagemDetail"),
    path('AreasJardinagemUpdate/<str:id_random>/', AreasJardinagemUpdate, name="AreasJardinagemUpdate"),
    path('AreasJardinagemAlterStatus/<str:id_random>/', AreasJardinagemAlterStatus, name="AreasJardinagemAlterStatus"),
    path('AreasAssociadasLocalidadeJardinagem/<str:id_random>/', AreasAssociadasLocalidadeJardinagem, name="AreasAssociadasLocalidadeJardinagem"),
    path('CreateAreaJardinagem/', CreateAreaJardinagem, name="CreateAreaJardinagem"),
    path('IfDeleteAreasJardinagem/<str:id_random>/', IfDeleteAreasJardinagem, name="IfDeleteAreasJardinagem"),
    path('ListAreasJardinagemFromFoms/', ListAreasJardinagemFromFoms.as_view(), name="ListAreasJardinagemFromFoms"),
    path('TempoDesdeUltimoAtendimentoJardinagem/', TempoDesdeUltimoAtendimentoJardinagem, name="TempoDesdeUltimoAtendimentoJardinagem"),
    path('DeleteAreasJardinagem/<str:id_random>/', DeleteAreasJardinagem, name="DeleteAreasJardinagem"),
]