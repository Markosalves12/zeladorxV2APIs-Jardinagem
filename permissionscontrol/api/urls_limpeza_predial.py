from django.urls import path
from permissionscontrol.api.views_limpeza_predial import (ListPermissionsLimpezaPredial,
                                                          ListPermissionsAccessLimpezaPredial,
                                                          PermissionsAccessLimpezaPredialUpdate,
                                                          PermissionsAccessLimpezaPredialDetail)


urlpatterns = [
    path('ListPermissionsLimpezaPredial/', ListPermissionsLimpezaPredial.as_view(), name="ListPermissionsLimpezaPredial"),
    path('ListPermissionsAccessLimpezaPredial/', ListPermissionsAccessLimpezaPredial.as_view(), name="ListPermissionsAccessLimpezaPredial"),
    path('PermissionsAccessLimpezaPredialUpdate/<str:id_random>/', PermissionsAccessLimpezaPredialUpdate, name="PermissionsAccessLimpezaPredialUpdate"),
    path('PermissionsAccessLimpezaPredialDetail/<str:id_random>/', PermissionsAccessLimpezaPredialDetail, name="PermissionsAccessLimpezaPredialDetail"),
]