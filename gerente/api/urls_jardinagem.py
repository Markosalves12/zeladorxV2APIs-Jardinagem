from django.urls import path
from gerente.api.views_jardinagem import (ListGerenteJardinagem,
                                          GerenteJardinagemDetail,
                                          GerenteJardinagemUpdate,
                                          GerenteJardinagemAlterStatus,
                                          CreateGerenteJardinagem, IfDeleteGerenteJardinagem,
                                          ListGerenteJardinagemFromForms, DeleteGerenteJardinagem)


urlpatterns = [
    path('ListGerenteJardinagem/', ListGerenteJardinagem.as_view(), name="ListGerenteJardinagem"),
    path('ListGerenteJardinagemFromForms/', ListGerenteJardinagemFromForms.as_view(), name="ListGerenteJardinagemFromForms"),
    path('CreateGerenteJardinagem/', CreateGerenteJardinagem, name="CreateGerenteJardinagem"),
    path('GerenteJardinagemDetail/<str:id_random>/', GerenteJardinagemDetail, name="GerenteJardinagemDetail"),
    path('GerenteJardinagemUpdate/<str:id_random>/', GerenteJardinagemUpdate, name="GerenteJardinagemUpdate"),
    path('GerenteJardinagemAlterStatus/<str:id_random>/', GerenteJardinagemAlterStatus, name="GerenteJardinagemAlterStatus"),
    path('IfDeleteGerenteJardinagem/<str:id_random>/', IfDeleteGerenteJardinagem, name="IfDeleteGerenteJardinagem"),
    path('DeleteGerenteJardinagem/<str:id_random>/', DeleteGerenteJardinagem, name="DeleteGerenteJardinagem"),
]