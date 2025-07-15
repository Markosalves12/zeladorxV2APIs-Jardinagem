from django.urls import path
from localidade.api.views_jardinagem import (ListLocalidadeJardins, LocalidadeJardinsDetail, LocalidadeJardinsUpdate,
                                             LocalidadeJardinsAlterStatus)


urlpatterns = [
    path('ListLocalidadeJardins/', ListLocalidadeJardins.as_view(), name="ListLocalidadeJardins"),
    path('LocalidadeJardinsDetail/<str:id_random>/', LocalidadeJardinsDetail, name="LocalidadeJardinsDetail"),
    path('LocalidadeJardinsUpdate/<str:id_random>/', LocalidadeJardinsUpdate, name="LocalidadeJardinsUpdate"),
    path('LocalidadeJardinsAlterStatus/<str:id_random>/', LocalidadeJardinsAlterStatus, name="LocalidadeJardinsAlterStatus"),
]