from django.urls import path
from permissionscontrol.api.views_jardinagem import (ListPermissionsJardinagem, ListPermissionsAccessJardinagem,
                                                     PermissionsAccessJardinagemUpdate, PermissionsAccessJardinagemDetail)


urlpatterns = [
    path('ListPermissionsJardinagem/', ListPermissionsJardinagem.as_view(), name="ListPermissionsJardinagem"),
    path('ListPermissionsAccessJardinagem/', ListPermissionsAccessJardinagem.as_view(), name="ListPermissionsAccessJardinagem"),
    path('PermissionsAccessJardinagemUpdate/<str:id_random>/', PermissionsAccessJardinagemUpdate, name="PermissionsAccessJardinagemUpdate"),
    path('PermissionsAccessJardinagemDetail/<str:id_random>/', PermissionsAccessJardinagemDetail, name="PermissionsAccessJardinagemDetail"),
]