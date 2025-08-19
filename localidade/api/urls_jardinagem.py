from django.urls import path
from localidade.api.views_jardinagem import (ListLocalidadeJardinagem, LocalidadeJardinagemDetail, LocalidadeJardinagemUpdate,
                                             LocalidadeJardinagemAlterStatus, CreateLocalidadeJardinagem,
                                             IfDeleteLocalidadeJardinagem, ListLocalidadeJardinagemFromForms,
                                             DeleteLocalidadeJardinagem)


urlpatterns = [
    path('ListLocalidadeJardinagem/', ListLocalidadeJardinagem.as_view(), name="ListLocalidadeJardinagem"),
    path('ListLocalidadeJardinagemFromForms/', ListLocalidadeJardinagemFromForms.as_view(), name="ListLocalidadeJardinagemFromForms"),
    path('LocalidadeJardinagemDetail/<str:id_random>/', LocalidadeJardinagemDetail, name="LocalidadeJardinagemDetail"),
    path('LocalidadeJardinagemUpdate/<str:id_random>/', LocalidadeJardinagemUpdate, name="LocalidadeJardinagemUpdate"),
    path('LocalidadeJardinagemAlterStatus/<str:id_random>/', LocalidadeJardinagemAlterStatus, name="LocalidadeJardinagemAlterStatus"),
    path('CreateLocalidadeJardinagem/', CreateLocalidadeJardinagem, name="CreateLocalidadeJardinagem"),
    path('IfDeleteLocalidadeJardinagem/<str:id_random>/', IfDeleteLocalidadeJardinagem, name="IfDeleteLocalidadeJardinagem"),
    path('DeleteLocalidadeJardinagem/<str:id_random>/', DeleteLocalidadeJardinagem, name="DeleteLocalidadeJardinagem"),
]