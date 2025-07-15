from django.urls import path
from permissionscontrol.api.views_especials import (ListPermissionsEspecials,ListPermissionsAccessEspecials,
                                                    PermissionsAccessEspecialsDetail, PermissionsAccessEspecialsUpdate)


urlpatterns = [
    path('ListPermissionsEspecials/', ListPermissionsEspecials.as_view(), name="ListPermissionsEspecials"),
    path('ListPermissionsAccessEspecials/', ListPermissionsAccessEspecials.as_view(), name="ListPermissionsAccessEspecials"),
    path('PermissionsAccessEspecialsDetail/<str:id_random>/', PermissionsAccessEspecialsDetail, name="PermissionsAccessEspecialsDetail"),
    path('PermissionsAccessEspecialsUpdate/<str:id_random>/', PermissionsAccessEspecialsUpdate, name="PermissionsAccessEspecialsUpdate"),
]