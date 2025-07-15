from django.urls import path
from gerente.api.views_jardinagem import ListGerenteJardins, GerenteJardinsDetail, GerenteJardinsUpdate, GerenteJardinsAlterStatus


urlpatterns = [
    path('ListGerenteJardins/', ListGerenteJardins.as_view(), name="ListGerenteJardins"),
    path('GerenteJardinsDetail/<str:id_random>/', GerenteJardinsDetail, name="GerenteJardinsDetail"),
    path('GerenteJardinsUpdate/<str:id_random>/', GerenteJardinsUpdate, name="GerenteJardinsUpdate"),
    path('GerenteJardinsAlterStatus/<str:id_random>/', GerenteJardinsAlterStatus, name="GerenteJardinsAlterStatus"),
]