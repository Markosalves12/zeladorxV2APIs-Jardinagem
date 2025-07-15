from django.urls import path
from areas.api.views_jardinagem import (ListAreasJardins, AreasJardinsDetail, AreasJardinsUpdate,
                                        AreasJardinsAlterStatus, AreasAssociadasLocalidadeJardins, CreateAreaJardins)


urlpatterns = [
    path('ListAreasJardins/', ListAreasJardins.as_view(), name="ListAreasJardins"),
    path('AreasJardinsDetail/<str:id_random>/', AreasJardinsDetail, name="AreasJardinsDetail"),
    path('AreasJardinsUpdate/<str:id_random>/', AreasJardinsUpdate, name="AreasJardinsUpdate"),
    path('AreasJardinsAlterStatus/<str:id_random>/', AreasJardinsAlterStatus, name="AreasJardinsAlterStatus"),
    path('AreasAssociadasLocalidadeJardins/<str:id_random>/', AreasAssociadasLocalidadeJardins, name="AreasAssociadasLocalidadeJardins"),
    path('CreateAreaJardins/', CreateAreaJardins, name="CreateAreaJardins"),
]